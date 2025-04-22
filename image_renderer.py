import matplotlib.pyplot as plt
import numpy as np

class LiveImageRenderer:
    @staticmethod
    def render(byte_array, width, height, delay=0.000000001):
        img_array = np.frombuffer(byte_array, dtype=np.uint8).reshape((height, width, 3))
        plt.imshow(img_array)
        plt.axis('off')
        plt.pause(delay)
        plt.clf()
