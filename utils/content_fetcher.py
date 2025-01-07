import requests
from bs4 import BeautifulSoup
from typing import Optional
import logging

class ContentFetcher:
    @staticmethod
    def fetch_url(url: str) -> Optional[str]:
        """获取URL内容"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 移除脚本和样式元素
            for script in soup(["script", "style"]):
                script.decompose()
                
            # 获取文本内容
            text = soup.get_text()
            # 清理文本
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            logging.error(f"Error fetching URL {url}: {str(e)}")
            return None 