from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # API设置
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    
    # 系统设置
    SYSTEM_NAME: str = "Tommy的人工智能知识大脑"
    SYSTEM_DESCRIPTION: str = "智能文本理解与音频处理系统"
    VERSION: str = "1.0.0"
    
    # 处理参数
    CHUNK_SIZE: int = 2000  # 文本分块大小
    OVERLAP_SIZE: int = 200  # 分块重叠大小
    MAX_TOKENS: int = 4096   # DeepSeek模型最大token数
    
    # 目录设置
    OUTPUT_DIR: str = "outputs"
    TEMP_DIR: str = "temp_audio"
    STATIC_DIR: str = "static"
    
settings = Settings() 