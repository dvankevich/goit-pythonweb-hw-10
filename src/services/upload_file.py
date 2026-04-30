import cloudinary
import cloudinary.uploader
import logging
from fastapi import HTTPException

from src.config.app_config import settings

logger = logging.getLogger(__name__)


class UploadFileService:
    """
    Сервіс для завантаження файлів в Cloudinary.
    """

    def __init__(self):
        """
        Ініціалізуємо Cloudinary один раз при створенні сервісу.
        Використовуємо розпакований SecretStr для api_secret.
        """
        self.cloud_name = settings.CLD_NAME
        self.api_key = settings.CLD_API_KEY
        self.api_secret = settings.CLD_API_SECRET.get_secret_value()

        # Налаштування Cloudinary
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

        logger.debug(f"Cloudinary configured for cloud: {self.cloud_name}")

    @staticmethod
    def upload_file(file, username: str) -> str:
        """
        Завантажує аватар користувача в Cloudinary.
        Повертає URL оптимізованого зображення (250x250).
        """
        try:
            public_id = f"RestApp/{username}"

            # Завантажуємо файл
            upload_result = cloudinary.uploader.upload(
                file.file, public_id=public_id, overwrite=True, resource_type="image"
            )

            # Генеруємо оптимізований URL
            optimized_url = cloudinary.CloudinaryImage(public_id).build_url(
                width=250, height=250, crop="fill", version=upload_result.get("version")
            )

            logger.info(f"Avatar successfully uploaded for user: {username}")
            return optimized_url

        except Exception as e:
            logger.error(f"Cloudinary upload failed for user {username}: {e}")
            raise HTTPException(
                status_code=500,
                detail="Не вдалося завантажити аватар. Спробуйте пізніше.",
            ) from e
