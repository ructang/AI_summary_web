from openai import OpenAI
from typing import Optional
from config import settings
import logging

class DeepSeekClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )
        
    def generate_summary(self, text: str) -> Optional[str]:
        """使用DeepSeek生成文本摘要"""
        try:
            prompt = f"""请对以下文本生成一个简洁的摘要，要求：
1. 保留核心观点和关键信息
2. 使用简明扼要的语言
3. 按重要性组织内容
4. 确保摘要的完整性和连贯性

原文：
{text}

摘要："""
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的文本摘要助手，善于提取文章重点，生成清晰简洁的摘要。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"调用DeepSeek API出错: {str(e)}")
            return None 