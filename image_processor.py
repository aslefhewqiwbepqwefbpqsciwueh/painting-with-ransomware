from PIL import Image
import numpy as np
import os
import io

class ImageProcessor:
    @staticmethod
    def create_gif_from_buffers(buffers, output_path, duration=300, loop=0):
        frames = []
        for buf in buffers:
            img = Image.open(buf).convert("RGB")
            img = img.convert("P", palette=Image.ADAPTIVE, colors=64)
            frames.append(img)
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            format='GIF',
            duration=duration,
            loop=loop,
            optimize=True,
            disposal=2
        )
    @staticmethod
    def stitch_buffers_horizontally(buffers):
        images = [Image.open(buf).convert("RGB") for buf in buffers]
        widths, heights = zip(*(img.size for img in images))

        total_width = sum(widths)
        max_height = max(heights)

        stitched_image = Image.new("RGB", (total_width, max_height))

        x_offset = 0
        for img in images:
            stitched_image.paste(img, (x_offset, 0))
            x_offset += img.width

        output_buffer = io.BytesIO()
        stitched_image.save(output_buffer, format="BMP")
        output_buffer.seek(0)

        return ImageProcessor.from_buffer(output_buffer)
    @classmethod
    def from_buffer(cls, buffer):
        instance = cls.__new__(cls)
        instance.original_path = None
        instance.byte_array = None
        instance.image_size = None
        instance.header_info = {}

        buffer.seek(0)
        img = Image.open(buffer).convert("RGB")
        instance.image_size = img.size
        instance.header_info = {
            "width": img.width,
            "height": img.height,
            "bits_per_pixel": 24
        }

        with io.BytesIO() as temp_buffer:
            img.save(temp_buffer, format="BMP")
            temp_buffer.seek(0)
            img = Image.open(temp_buffer)
            instance.byte_array = img.tobytes()

        return instance
    @staticmethod
    def save_buffer_to_file(buffer, output_path):
        with open(output_path, 'wb') as f:
            f.write(buffer.getvalue())


    SUPPORTED_FORMATS = {"png", "jpg", "jpeg", "bmp"}

    def __init__(self, image_path):
        self.original_path = image_path
        self.byte_array = None
        self.image_size = None
        self.header_info = {}

        self._validate_image()
        self._load_and_process_image()

    def _validate_image(self):
        if not os.path.exists(self.original_path):
            raise FileNotFoundError(f"File not found: {self.original_path}")

        ext = self.original_path.split('.')[-1].lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {ext}. Supported formats: {self.SUPPORTED_FORMATS}")

    def _load_and_process_image(self):
        # Open and convert to RGB
        img = Image.open(self.original_path).convert("RGB")
        self.image_size = img.size
        self.header_info = {
            "width": img.width,
            "height": img.height,
            "bits_per_pixel": 24
        }

        # Extract raw RGB bytes
        with io.BytesIO() as buffer:
            img.save(buffer, format="BMP")
            buffer.seek(0)
            img = Image.open(buffer)
            self.byte_array = img.tobytes()

    def reconstruct_bmp(self, byte_array, output_path=None):
        width = self.header_info["width"]
        height = self.header_info["height"]

        expected_size = height * width * 3
        if len(byte_array) != expected_size:
            byte_array = byte_array[:expected_size]  # trim extra padding due to block modes of encryption
        img_array = np.frombuffer(byte_array, dtype=np.uint8).reshape((height, width, 3))
        img = Image.fromarray(img_array, "RGB")

        buffer = io.BytesIO()
        img.save(buffer, format="BMP")
        buffer.seek(0)

        if output_path:
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())

        return buffer
