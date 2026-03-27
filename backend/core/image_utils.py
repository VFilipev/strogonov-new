
import base64
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def generate_placeholder_base64(image_field, quality=50):
    if not image_field or not image_field.name:
        return None

    try:
        img = Image.open(image_field)

        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=quality, method=6)
        buffer.seek(0)

        base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/webp;base64,{base64_str}"

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Ошибка генерации placeholder: {e}")
        return None


def generate_placeholder_file(image_field, upload_to, quality=50):
    if not image_field or not image_field.name:
        return None

    try:
        img = Image.open(image_field)

        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=quality, method=6)
        buffer.seek(0)

        original_name = image_field.name
        name_without_ext = original_name.rsplit('.', 1)[0]
        filename = f"{name_without_ext}_placeholder.webp"
        filepath = f"{upload_to}{filename}"

        file_content = ContentFile(buffer.getvalue())
        saved_path = default_storage.save(filepath, file_content)

        return saved_path

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Ошибка генерации placeholder файла: {e}")
        return None

