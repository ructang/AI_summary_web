import requests
from bs4 import BeautifulSoup
import logging

class ContentFetcher:
    def fetch_url(self, url: str) -> str:
        """获取URL内容"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # 使用BeautifulSoup解析内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 移除脚本和样式元素
            for script in soup(["script", "style"]):
                script.decompose()
                
            # 获取文本
            text = soup.get_text()
            
            # 处理文本
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            logging.error(f"获取URL内容失败: {str(e)}")
            return "" 