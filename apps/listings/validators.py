from pathlib import Path

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


ALLOWED_LISTING_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_LISTING_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_LISTING_PHOTO_BYTES = 5 * 1024 * 1024

INVALID_EXTENSION_MESSAGE = "Seuls les fichiers JPEG, PNG ou WebP sont acceptes."
EMPTY_FILE_MESSAGE = "Le fichier photo est vide."
TOO_LARGE_MESSAGE = "La photo depasse la taille maximale autorisee."
INVALID_IMAGE_MESSAGE = "Le fichier doit etre une image JPEG, PNG ou WebP valide."


def validate_listing_photo_upload(uploaded_file):
    extension = Path(getattr(uploaded_file, "name", "")).suffix.lower()
    if extension not in ALLOWED_LISTING_IMAGE_EXTENSIONS:
        raise ValidationError(INVALID_EXTENSION_MESSAGE, code="invalid_extension")

    size = getattr(uploaded_file, "size", 0)
    if size == 0:
        raise ValidationError(EMPTY_FILE_MESSAGE, code="empty")
    if size > MAX_LISTING_PHOTO_BYTES:
        raise ValidationError(TOO_LARGE_MESSAGE, code="too_large")

    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        image.verify()
    except (UnidentifiedImageError, OSError, ValueError) as error:
        raise ValidationError(INVALID_IMAGE_MESSAGE, code="invalid_image") from error
    finally:
        uploaded_file.seek(0)

    if image.format not in ALLOWED_LISTING_IMAGE_FORMATS:
        raise ValidationError(INVALID_IMAGE_MESSAGE, code="invalid_image")

    return uploaded_file
