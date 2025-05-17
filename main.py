from image_processor import ImageProcessor
from encryption import EncryptionEngine, Ransomware

processor = ImageProcessor("images/milhouse.png")

engine = EncryptionEngine(
    mode=Ransomware.LOO_CIPHER,
    seed=2
)

encrypted = engine.encrypt(processor.byte_array)
buffer = processor.reconstruct_bmp(encrypted)

# Save output
ImageProcessor.save_buffer_to_file(buffer, "images/output.bmp")
