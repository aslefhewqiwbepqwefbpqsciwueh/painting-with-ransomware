import sys
from image_processor import ImageProcessor
from encryption import EncryptionEngine, Ransomware
from cellular_encryptor import CellularAutomataEncryptor

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        output_path = "images/encrypted_output.bmp"
        list_of_buffers = []

        processor = ImageProcessor(image_path)
        seed_var = 150
        engine = CellularAutomataEncryptor(
            width=processor.header_info['width'],
            height=processor.header_info['height'],
            seed=90
        )
        engine.run()
        encrypted_bytes = engine.apply_to_image(processor.byte_array)
        # engine = EncryptionEngine(
        #     mode=Ransomware.RC4_KSA_STRETCH,  # Change as needed
        #     grayscale=False,
        #     reverse=False,
        #     seed=seed_var
        # )
        # encrypted_bytes = engine.encrypt(processor.byte_array)
        new_image_1 = processor.reconstruct_bmp(encrypted_bytes)
        list_of_buffers.append(new_image_1)
        seed_var += 1

        ImageProcessor.save_buffer_to_file(new_image_1, output_path)
        print(f"Encrypted image saved as: {output_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
