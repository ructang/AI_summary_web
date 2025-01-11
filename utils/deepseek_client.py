import openai
from typing import Optional
from config import settings
import logging
import time

class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        if not self.api_key:
            raise ValueError("未设置 DEEPSEEK_API_KEY")
            
        openai.api_key = self.api_key
        openai.api_base = "https://api.deepseek.com/v1"
        
    def generate_summary(self, text: str, max_retries: int = 3) -> Optional[str]:
        """使用DeepSeek生成文本摘要"""
        if not text:
            logging.error("输入文本为空")
            return None
            
        logging.info(f"开始生成摘要，文本长度: {len(text)}")
        
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
        
        for attempt in range(max_retries):
            try:
                logging.info(f"尝试调用 DeepSeek API (第 {attempt + 1} 次)")
                
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
                
                summary = response.choices[0].message.content.strip()
                logging.info(f"成功生成摘要，长度: {len(summary)}")
                return summary
                
            except openai.error.RateLimitError:
                wait_time = (attempt + 1) * 5
                logging.warning(f"API 速率限制，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                
            except openai.error.APIError as e:
                logging.error(f"API 错误: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                raise
                
            except Exception as e:
                error_msg = f"调用 DeepSeek API 出错: {str(e)}"
                logging.error(error_msg)
                raise RuntimeError(error_msg)
                
        logging.error(f"在 {max_retries} 次尝试后仍未成功生成摘要")
        return None 