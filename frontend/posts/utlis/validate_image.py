import base64
cover_image_size = 5 * 1024 * 1024


def validate_cover_image(cover_image):
    errors = ''
    if cover_image.size > cover_image_size:
        errors += "Cover image must be less than 5MB."

    # Check file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if cover_image.content_type not in allowed_types:
        errors += "Cover image must be a valid image file (JPEG, PNG, GIF, WebP)."

    return errors


def convert_image_to_base64(cover_image):
    # Convert image to base64
    image_data = cover_image.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    base64_image = {
        'name': cover_image.name,
        'content': image_base64,
        'content_type': cover_image.content_type,
        'size': cover_image.size
    }
    return base64_image
