from minio import Minio
import logging
from config import settings

class CloudStorage:
    def __init__(self):
        self.client = Minio(
            settings.STORAGE_ENDPOINT,
            access_key=settings.STORAGE_ACCESS_KEY,
            secret_key=settings.STORAGE_SECRET_KEY,
            secure=True
        )
    
    def save_file(self, file_data, file_name):
        bucket_name = "summaries"
        try:
            self.client.put_object(
                bucket_name,
                file_name,
                file_data,
                len(file_data)
            )
            return f"{settings.STORAGE_ENDPOINT}/{bucket_name}/{file_name}"
        except Exception as e:
            logging.error(f"保存文件失败: {str(e)}")
            return None 