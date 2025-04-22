from enum import Enum, auto
import random
import hashlib
import numpy as np

class CellularAutomataEncryptor:
    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        self.seed = seed
        self.rule = seed % 256  # Rule from 0 to 255
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.rule_map = self._generate_rule_map()

    def _generate_rule_map(self):
        # Create a mapping for the 8 possible 3-bit neighborhoods
        binary_rule = format(self.rule, '08b')
        return {
            (1, 1, 1): int(binary_rule[0]),
            (1, 1, 0): int(binary_rule[1]),
            (1, 0, 1): int(binary_rule[2]),
            (1, 0, 0): int(binary_rule[3]),
            (0, 1, 1): int(binary_rule[4]),
            (0, 1, 0): int(binary_rule[5]),
            (0, 0, 1): int(binary_rule[6]),
            (0, 0, 0): int(binary_rule[7]),
        }

    def _initial_row(self):
        row = np.zeros(self.width, dtype=np.uint8)
        # Seed initial row with active bits at edges and center
        row[0] = 1
        row[self.width // 2] = 1
        row[-1] = 1
        return row

    def run(self):
        self.grid[0] = self._initial_row()
        for y in range(1, self.height):
            for x in range(self.width):
                left = self.grid[y-1][(x - 1) % self.width]
                center = self.grid[y-1][x]
                right = self.grid[y-1][(x + 1) % self.width]
                self.grid[y][x] = self.rule_map[(left, center, right)]
        return self.grid

    def apply_to_image_random_rgb(self, byte_array):
        mask = self.grid.flatten()
        encrypted = bytearray()
        rng = random.Random(self.seed)
        for i in range(0, len(byte_array), 3):
            index = i // 3
            if index < len(mask) and mask[index]:
                key = [rng.randint(0, 255) for _ in range(3)]
                encrypted.extend([b ^ k for b, k in zip(byte_array[i:i+3], key)])
            else:
                encrypted.extend(byte_array[i:i+3])
        return encrypted

    def apply_to_image(self, byte_array):
        mask = self.grid.flatten()
        encrypted = bytearray()
        for i in range(0, len(byte_array), 3):
            index = i // 3
            if index < len(mask) and mask[index]:
                encrypted.extend([b ^ 0xFF for b in byte_array[i:i+3]])
            else:
                encrypted.extend(byte_array[i:i+3])
        return encrypted
