
from PIL import Image, ImageFilter
from imagekit.processors import ResizeToFill, ResizeToFit


class SmartCropProcessor(ResizeToFill):
    def process(self, img):
        return super().process(img)


class NoOpProcessor:

    def process(self, img):

        return img


class ResizeToFitWithPadding(ResizeToFit):
    def __init__(self, width, height, background_color=(255, 255, 255, 0)):
        super().__init__(width, height)
        self.background_color = background_color

    def process(self, img):

        original_width, original_height = img.size
        target_width, target_height = self.width, self.height

        scale = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        if img.mode == 'RGBA':
            new_img = Image.new('RGBA', (target_width, target_height), self.background_color)
        else:
            new_img = Image.new('RGB', (target_width, target_height), self.background_color[:3])
            resized = resized.convert('RGB')

        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        new_img.paste(resized, (x_offset, y_offset))

        return new_img

