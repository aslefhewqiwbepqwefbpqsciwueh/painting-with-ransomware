from enum import Enum, auto
import random
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from image_renderer import LiveImageRenderer

class Ransomware(Enum):
    LOO_CIPHER = auto()
    PRINCE = auto()
    PRINCE_SHIFTED = auto()
    ECB_CLASSIC = auto()
    XOR_SIMPLE = auto()
    XOR_BASIC = auto()
    MT_XOR = auto()
    MT_STATE_XOR = auto()
    RC4 = auto()
    RC4_KSA = auto()
    RC4_KSA_STRETCH = auto()

class EncryptionEngine:
    def __init__(self, mode=Ransomware.ECB_CLASSIC, grayscale=False, reverse=False, seed=None, block_size=48, render=False, width=None, height=None):
        self.mode = mode
        self.grayscale = grayscale
        self.reverse = reverse
        self.seed = seed
        self.block_size = block_size
        self.render = render
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(seed)

    def encrypt(self, byte_array):
        encrypted = self._apply_ransomware_mode(byte_array)

        if self.grayscale:
            encrypted = self._to_grayscale(encrypted)

        if self.reverse:
            encrypted = encrypted[::-1]

        return encrypted

    def _apply_ransomware_mode(self, byte_array):
        if self.mode == Ransomware.LOO_CIPHER:
            return self._loocipher_encrypt(byte_array)
        elif self.mode == Ransomware.PRINCE:
            return self._prince_encrypt(byte_array)
        elif self.mode == Ransomware.PRINCE_SHIFTED:
            return self._prince_shifted_encrypt(byte_array)
        elif self.mode == Ransomware.ECB_CLASSIC:
            return self._ecb_style_encrypt(byte_array)
        elif self.mode == Ransomware.XOR_SIMPLE:
            return self._xor_encrypt(byte_array)
        elif self.mode == Ransomware.XOR_BASIC:
            return self._xor_basic_encrypt(byte_array)
        elif self.mode == Ransomware.MT_XOR:
            return self._mt_xor_encrypt(byte_array)
        elif self.mode == Ransomware.MT_STATE_XOR:
            return self._mt_state_xor_encrypt(byte_array)
        elif self.mode == Ransomware.RC4:
            return self._rc4_encrypt(byte_array)
        elif self.mode == Ransomware.RC4_KSA:
            return self._rc4_ksa_encrypt(byte_array)
        elif self.mode == Ransomware.RC4_KSA_STRETCH:
            return self._rc4_ksa_stretch_encrypt(byte_array)
        else:
            raise ValueError(f"Unsupported ransomware mode: {self.mode}")

    def _loocipher_encrypt(self, data):
        print("Encrypting using LooCipher logic...")
        charset = "!@#%&?+-*/=_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        if self.seed is None:
            raise ValueError("LooCipher mode requires a seed to be set.")

        rng = random.Random(self.seed)
        key = ''.join(rng.choice(charset) for _ in range(16)).encode('utf-8')

        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()

        encrypted = bytearray()

        for i in range(0, len(data), 16):
            block = data[i:i+16]
            if len(block) < 16:
                block = block.ljust(16, b'\x00')
            encrypted_block = encryptor.update(block)
            encrypted.extend(encrypted_block)
            if self.render:
                # Create a copy of the full original image to work with
                temp_frame = bytearray(data)

                # Fill in encrypted regions
                for i in range(len(encrypted)):
                    temp_frame[i] = encrypted[i]

                # Then render
                LiveImageRenderer.render(temp_frame, self.width, self.height)

        encrypted.extend(encryptor.finalize())
        return encrypted

    def _prince_encrypt(self, data):
        print("Encrypting using Prince Ransomware logic...")

        if self.seed is None:
            raise ValueError("PRINCE mode requires a seed to be set.")

        # Use seed to derive a deterministic ChaCha20-like key and nonce
        seed_bytes = hashlib.sha256(str(self.seed).encode()).digest()
        key = seed_bytes[:32]   # Using 256-bit key for ChaCha20
        nonce = seed_bytes[16:32]  # Using 128-bit nonce due to cryptography library constraints

        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        encryptor = cipher.encryptor()

        encrypted = bytearray()
        i = 0
        while i < len(data):
            if i % 3 == 0:
                encrypted.append(encryptor.update(bytes([data[i]]))[0])
            else:
                encrypted.append(data[i])
            i += 1

        return encrypted

    def _prince_shifted_encrypt(self, data):
        print("Encrypting using Prince Ransomware logic...")

        if self.seed is None:
            raise ValueError("PRINCE mode requires a seed to be set.")

        # Use seed to derive a deterministic ChaCha20-like key and nonce
        seed_bytes = hashlib.sha256(str(self.seed).encode()).digest()
        key = seed_bytes[:32]   # Using 256-bit key for ChaCha20
        nonce = seed_bytes[16:32]  # Using 128-bit nonce due to cryptography library constraints

        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        index = self.seed % 3
        length_original_data = len(data)
        data = data[index:]
        encrypted = bytearray()
        i = 0
        while i < len(data):
            if i % 3 == 0:
                encrypted.append(encryptor.update(bytes([data[i]]))[0])
            else:
                encrypted.append(data[i])
            i += 1

        encrypted = encrypted.ljust(length_original_data, b'\x00')
        return encrypted

    def _ecb_style_encrypt(self, data):
        print("Encrypting using ECB-style logic...")

        block_size = self.block_size
        encrypted = bytearray()
        block_map = {}

        for i in range(0, len(data), block_size):
            block = data[i:i + block_size]

            if len(block) < block_size:
                block = block.ljust(block_size, b'\x00')

            key = hashlib.md5(block).digest()

            if key not in block_map:
                scrambled = bytearray((b ^ key[j % len(key)]) for j, b in enumerate(block))
                block_map[key] = scrambled

            encrypted.extend(block_map[key])

        return encrypted

    def _xor_encrypt(self, data):
        print("Encrypting using XOR-simple logic...")
        if self.seed is None:
            raise ValueError("XOR_SIMPLE mode requires a seed to be set.")

        key = hashlib.sha256(str(self.seed).encode()).digest()
        return bytearray((b ^ key[i % len(key)]) for i, b in enumerate(data))

    def _xor_basic_encrypt(self, data):
        print("Encrypting using XOR-basic logic...")
        if self.seed is None:
            raise ValueError("XOR_BASIC mode requires a seed to be set.")

        key = self.seed % 256
        return bytearray((b ^ key) for b in data)

    def _mt_xor_encrypt(self, data):
        print("Encrypting using Mersenne Twister XOR logic...")
        if self.seed is None:
            raise ValueError("MT_XOR mode requires a seed to be set.")

        rng = random.Random(self.seed)
        return bytearray((b ^ rng.getrandbits(8)) for b in data)

    def _mt_state_xor_encrypt(self, data):
        print("Encrypting using Mersenne Twister state array XOR logic...")
        if self.seed is None:
            raise ValueError("MT_STATE_XOR mode requires a seed to be set.")

        rng = random.Random(self.seed)
        state = rng.getstate()
        state_array = state[1]

        xor_stream = []
        for word in state_array:
          xor_stream.append(word % 0xA0) #This modulo can be edited to increase or decrease a damping factor on the encryption


        encrypted = bytearray()
        for i, b in enumerate(data):
            encrypted.append(b ^ xor_stream[i % len(xor_stream)])

        return encrypted

    def _rc4_encrypt(self, data):
        print("Encrypting using RC4 logic...")
        if self.seed is None:
            raise ValueError("RC4 mode requires a seed to be set.")

        key = bytearray(str(self.seed).encode())
        S = list(range(256))
        j = 0

        # KSA (Key Scheduling Algorithm)
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        # PRGA (Pseudo-Random Generation Algorithm)
        i = j = 0
        keystream = []
        for _ in range(len(data)):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            keystream.append(K)

        return bytearray((b ^ keystream[n]) for n, b in enumerate(data))

    def _rc4_ksa_encrypt(self, data):
        print("Encrypting using RC4 KSA-only logic...")
        S = list(range(256))
        encrypted = bytearray()

        for i, b in enumerate(data):
            encrypted.append(b ^ S[i % 256])

        return encrypted

    def _rc4_ksa_stretch_encrypt(self, data):
        print("Encrypting using RC4 KSA-stretch logic...")
        length = len(data)
        stretched = [int((i / length) * 255) for i in range(length)]

        encrypted = bytearray()
        for i, b in enumerate(data):
            encrypted.append(b ^ stretched[i])

        return encrypted

    def _to_grayscale(self, data):
        print("Applying grayscale filter...")
        gray_data = bytearray()
        for i in range(0, len(data), 3):
            if i + 2 >= len(data):
                break
            r, g, b = data[i], data[i+1], data[i+2]
            avg = int((r + g + b) / 3)
            gray_data.extend([avg, avg, avg])
        return gray_data
