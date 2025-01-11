from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # 基础配置
    SYSTEM_NAME = "Tommy的人工智能知识大脑"
    SYSTEM_DESCRIPTION = "智能文本理解与音频处理系统"
    VERSION = "1.0.0"
    
    # 处理参数
    CHUNK_SIZE = 2000
    OUTPUT_DIR = "outputs"
    TEMP_DIR = "temp_audio"
    
    # API配置
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    
    # 存储配置
    STORAGE_ENDPOINT = os.getenv('STORAGE_ENDPOINT')
    STORAGE_ACCESS_KEY = os.getenv('STORAGE_ACCESS_KEY')
    STORAGE_SECRET_KEY = os.getenv('STORAGE_SECRET_KEY')
    
    # Redis配置
    REDIS_URL = os.getenv('REDIS_URL')

settings = Settings() 