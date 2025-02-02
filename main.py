import os
import logging
from utils.content_fetcher import ContentFetcher
from utils.text_splitter import TextSplitter
from utils.deepseek_client import DeepSeekClient
from utils.audio_processor import AudioProcessor
from config import settings
import mimetypes
import requests
from celery import Celery

logging.basicConfig(level=logging.INFO)

# 配置Celery
celery = Celery('main')

# 首先加载基本配置
celery.config_from_object('celery_config')

# 然后确保关键配置被正确设置
app_config = {
    'broker_url': settings.REDIS_URL,
    'result_backend': settings.REDIS_URL,
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'Asia/Shanghai',
    'task_track_started': True,
    'worker_pool': 'solo',
    'broker_connection_retry_on_startup': True,
    'worker_max_tasks_per_child': 1,
    'worker_prefetch_multiplier': 1,
    'worker_concurrency': 1,
    'task_acks_late': True,
    'task_reject_on_worker_lost': True
}

celery.conf.update(app_config)

@celery.task(bind=True, name='main.process_content')
def process_content(self, url):
    try:
        logging.info(f"开始处理URL: {url}")
        self.update_state(state='PROGRESS', meta={'message': '正在初始化...'})
        
        summarizer = ContentSummarizer()
        result = summarizer.process_url(url)
        
        logging.info("处理完成")
        return {"status": "success", "result": result}
    except Exception as e:
        logging.error(f"处理失败: {str(e)}", exc_info=True)
        return {"status": "error", "message": str(e)}

class ContentSummarizer:
    def __init__(self):
        self.content_fetcher = ContentFetcher()
        self.text_splitter = TextSplitter()
        self.deepseek_client = DeepSeekClient()
        self.audio_processor = AudioProcessor()
        self.settings = settings
        
        # 创建输出目录
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        
    def process_url(self, url: str) -> str:
        """处理URL内容并生成摘要"""
        # 判断URL类型
        content_type = self._get_content_type(url)
        
        # 获取内容
        if self._is_audio_type(content_type) or "youtube.com" in url or "youtu.be" in url:
            logging.info("检测到音频内容，开始处理...")
            content = self.audio_processor.process_url(url)
            if not content:
                raise ValueError(f"无法处理音频内容: {url}")
        else:
            logging.info("检测到文本内容，开始处理...")
            content = self.content_fetcher.fetch_url(url)
            if not content:
                raise ValueError(f"无法获取URL内容: {url}")
            
        # 分割文本
        chunks = self.text_splitter.split_text(content)
        
        # 为每个块生成摘要
        summaries = []
        for i, chunk in enumerate(chunks):
            logging.info(f"处理第 {i+1}/{len(chunks)} 块")
            summary = self.deepseek_client.generate_summary(chunk)
            if summary:
                summaries.append(summary)
                
        # 合并所有摘要
        final_summary = "\n\n".join(summaries)
        
        # 保存结果
        output_file = os.path.join(settings.OUTPUT_DIR, "summary.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_summary)
            
        return final_summary
        
    def _get_content_type(self, url: str) -> str:
        """获取URL内容类型"""
        try:
            response = requests.head(url)
            return response.headers.get('content-type', '')
        except:
            # 如果无法获取，则通过文件扩展名判断
            return mimetypes.guess_type(url)[0] or ''
            
    def _is_audio_type(self, content_type: str) -> bool:
        """判断是否为音频类型"""
        return any(t in content_type.lower() for t in ['audio', 'video', 'mpeg', 'mp3', 'mp4', 'wav'])

def main():
    summarizer = ContentSummarizer()
    url = input("请输入要处理的URL: ")
    try:
        summary = summarizer.process_url(url)
        print("\n生成的摘要：")
        print(summary)
        print(f"\n摘要已保存到: {os.path.join(settings.OUTPUT_DIR, 'summary.txt')}")
    except Exception as e:
        logging.error(f"处理过程中出错: {str(e)}")

if __name__ == "__main__":
    main() 