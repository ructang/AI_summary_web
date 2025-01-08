from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # API设置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    
    # 系统设置
    SYSTEM_NAME = "Tommy的人工智能知识大脑"
    SYSTEM_DESCRIPTION = "智能文本理解与音频处理系统"
    VERSION = "1.0.0"
    
    # 处理参数
    CHUNK_SIZE = 2000  # 文本分块大小
    OVERLAP_SIZE = 200  # 分块重叠大小
    MAX_TOKENS = 4096   # DeepSeek模型最大token数
    
    # 目录设置
    OUTPUT_DIR = "outputs"
    TEMP_DIR = "temp_audio"
    STATIC_DIR = "static"
    
settings = Settings() 