import openai
from typing import Optional
from config import settings
import logging

class DeepSeekClient:
    def __init__(self):
        openai.api_key = settings.DEEPSEEK_API_KEY
        openai.api_base = "https://api.deepseek.com/v1"
        
    def generate_summary(self, text: str) -> Optional[str]:
        """使用DeepSeek生成文本摘要"""
        try:
            prompt = f"""请对以下文本进行全面的信息提取和结构化总结，要求：

1. 核心信息提取：
   - 提取文章中的关键事实、数据和观点
   - 确保信息的准确性和完整性
   - 保留重要的数字、日期、人名等具体信息

2. 结构化呈现：
   - 使用清晰的层级结构和编号
   - 按主题或时间顺序分类整理
   - 用要点形式列出，确保不重不漏

3. 重要细节保留：
   - 保留关键的背景信息
   - 记录重要的原因和结果
   - 突出特殊或独特的观点

4. 总结原则：
   - 保持客观准确
   - 避免过度概括
   - 确保信息可追溯
   - 突出信息的逻辑关系

原文：
{text}

结构化摘要："""
            
            response = openai.ChatCompletion.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的文本分析专家，擅长结构化信息提取和逻辑梳理。你的工作是将文本内容转化为清晰、完整、有条理的要点列表，确保信息的完整性和可追溯性。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3,
                top_p=0.95,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"调用DeepSeek API出错: {str(e)}")
            return None 