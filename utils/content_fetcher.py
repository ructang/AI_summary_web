import requests
from bs4 import BeautifulSoup
import logging
import re
import time
import json
from typing import Optional
from urllib.parse import urljoin

class ContentFetcher:
    def fetch_url(self, url: str, max_retries: int = 3) -> str:
        """获取URL内容"""
        # 检查是否是36kr的文章
        if '36kr.com/p/' in url:
            article_id = url.split('/p/')[-1].split('/')[0].split('?')[0]
            content = self._fetch_36kr_content(article_id)
            if content:
                return content
                
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 设置通用请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8,application/json',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'DNT': '1'
                }
                
                # 发送请求
                logging.info(f"开始获取URL内容 (第 {attempt + 1} 次尝试): {url}")
                session = requests.Session()
                response = session.get(url, headers=headers, timeout=30, verify=False)
                response.raise_for_status()
                
                logging.info(f"请求状态码: {response.status_code}")
                logging.info(f"响应头: {response.headers}")
                
                # 检查是否是JSON响应
                content_type = response.headers.get('content-type', '').lower()
                logging.info(f"内容类型: {content_type}")
                
                if 'application/json' in content_type:
                    try:
                        json_data = response.json()
                        content = self._extract_content_from_json(json_data)
                        if content:
                            return content
                    except Exception as e:
                        logging.warning(f"JSON解析失败: {str(e)}")
                
                # 智能设置编码
                if response.encoding == 'ISO-8859-1' or not response.encoding:
                    detected_encoding = response.apparent_encoding
                    logging.info(f"检测到编码: {detected_encoding}")
                    response.encoding = detected_encoding or 'utf-8'
                
                # 解析页面
                logging.info("成功获取页面内容，开始解析...")
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 移除干扰元素
                for element in soup(["script", "style", "meta", "link", "header", "footer", "nav", "iframe", "noscript", "ins", "aside", "form"]):
                    element.decompose()
                
                # 多策略内容提取
                content_candidates = []
                
                # 策略1: 通过通用选择器查找
                selectors = [
                    'article', 'main', '[role="main"]', '[role="article"]',
                    '.article', '.content', '.post', '#content', '#main',
                    '.article-content', '.post-content', '.entry-content',
                    '.detail-content', '.article-detail', '.main-content'
                ]
                
                for selector in selectors:
                    elements = soup.select(selector)
                    if elements:
                        logging.info(f"找到选择器 {selector} 的元素数量: {len(elements)}")
                        for element in elements:
                            content_candidates.append({
                                'text': element.get_text(separator='\n'),
                                'length': len(element.get_text()),
                                'source': f'selector:{selector}'
                            })
                
                # 策略2: 查找最大文本块
                text_blocks = self._find_text_blocks(soup)
                for block in text_blocks:
                    content_candidates.append({
                        'text': block.get_text(separator='\n'),
                        'length': len(block.get_text()),
                        'source': 'text_block'
                    })
                
                # 策略3: 使用整个body作为候选
                if soup.body:
                    content_candidates.append({
                        'text': soup.body.get_text(separator='\n'),
                        'length': len(soup.body.get_text()),
                        'source': 'body'
                    })
                
                # 选择最佳候选内容
                if content_candidates:
                    # 按长度排序
                    content_candidates.sort(key=lambda x: x['length'], reverse=True)
                    # 记录候选内容信息
                    for i, candidate in enumerate(content_candidates[:3]):
                        logging.info(f"候选内容 {i+1}: 来源={candidate['source']}, 长度={candidate['length']}")
                    
                    # 选择最长的有效内容
                    for candidate in content_candidates:
                        text = self._clean_text(candidate['text'])
                        if text and len(text) >= 50:  # 基本有效性验证
                            logging.info(f"选择来源 {candidate['source']} 的内容，清理后长度: {len(text)}")
                            return text
                
                raise ValueError("未能找到有效的文本内容")
                
            except requests.Timeout:
                last_error = f"请求超时: {url}"
                logging.warning(f"{last_error}，第 {attempt + 1} 次尝试")
                time.sleep(2 * (attempt + 1))
                
            except requests.RequestException as e:
                last_error = f"网络请求失败: {str(e)}"
                logging.warning(f"{last_error}，第 {attempt + 1} 次尝试")
                time.sleep(2 * (attempt + 1))
                
            except Exception as e:
                last_error = f"获取URL内容失败: {str(e)}"
                logging.warning(f"{last_error}，第 {attempt + 1} 次尝试")
                time.sleep(2 * (attempt + 1))
        
        error_msg = f"在 {max_retries} 次尝试后仍未成功获取内容: {last_error}"
        logging.error(error_msg)
        raise RuntimeError(error_msg)
    
    def _find_text_blocks(self, soup):
        """查找页面中的文本块"""
        blocks = []
        for element in soup.find_all(['div', 'article', 'section', 'main', 'p']):
            # 计算文本密度
            text = element.get_text(separator=' ', strip=True)
            if not text:
                continue
            
            # 计算html长度（包括标签）
            html_length = len(str(element))
            if html_length == 0:
                continue
            
            # 文本密度 = 文本长度 / HTML长度
            density = len(text) / html_length
            
            # 文本行数
            lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 10]
            
            # 选择文本密度高且包含多行的块
            if density > 0.5 and len(lines) > 3:
                blocks.append(element)
        
        return blocks
    
    def _clean_text(self, text: str) -> str:
        """清理和规范化文本"""
        # 分行处理
        lines = []
        for line in text.splitlines():
            line = line.strip()
            # 保留有意义的行
            if line and len(line) > 10 and not any(x in line.lower() for x in [
                'copyright', '版权所有', '举报', '投诉', '关注我们', '扫描二维码',
                '添加微信', '联系我们', '广告合作', '免责声明'
            ]):
                lines.append(line)
        
        # 合并文本
        text = '\n'.join(lines)
        
        # 清理格式
        text = re.sub(r'\s+', ' ', text).strip()  # 清理多余空白
        text = re.sub(r'([。！？；])\s*', r'\1\n', text)  # 在句子结束符后添加换行
        text = re.sub(r'\n\s*\n', '\n', text)  # 清理多余换行
        
        return text.strip()
    
    def _extract_content_from_json(self, data, depth=0, max_depth=5):
        """从JSON数据中提取可能的文章内容"""
        if depth > max_depth:
            return None
            
        if isinstance(data, str) and len(data) > 100:
            return data
            
        if isinstance(data, dict):
            # 可能包含内容的键名
            content_keys = ['content', 'article', 'text', 'body', 'data', 'detail', 'message']
            for key in content_keys:
                if key in data:
                    result = self._extract_content_from_json(data[key], depth + 1)
                    if result:
                        return result
                        
            # 递归搜索所有值
            for value in data.values():
                result = self._extract_content_from_json(value, depth + 1)
                if result:
                    return result
                    
        if isinstance(data, list):
            # 尝试合并所有文本内容
            texts = []
            for item in data:
                result = self._extract_content_from_json(item, depth + 1)
                if result:
                    texts.append(result)
            if texts:
                return '\n'.join(texts)
                
        return None 
    
    def _fetch_36kr_content(self, article_id: str) -> Optional[str]:
        """获取36kr文章内容"""
        try:
            # 设置通用请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Pragma': 'no-cache'
            }
            
            # 首先获取网页内容来获取必要的token
            web_url = f"https://www.36kr.com/p/{article_id}"
            logging.info(f"获取36kr网页内容: {web_url}")
            
            session = requests.Session()
            web_response = session.get(web_url, headers=headers, timeout=30, verify=False)
            logging.info(f"网页请求状态码: {web_response.status_code}")
            
            if web_response.status_code == 200:
                # 尝试从网页中提取内容
                soup = BeautifulSoup(web_response.text, 'html.parser')
                
                # 查找script标签中的数据
                scripts = soup.find_all('script')
                initial_state = None
                for script in scripts:
                    if script.string and 'window.__INITIAL_STATE__' in script.string:
                        try:
                            # 提取JSON数据
                            json_str = script.string.split('window.__INITIAL_STATE__=')[-1].split(';')[0]
                            initial_state = json.loads(json_str)
                            logging.info("成功提取到初始状态数据")
                            break
                        except Exception as e:
                            logging.warning(f"解析初始状态数据失败: {str(e)}")
                
                if initial_state:
                    # 从初始状态中提取文章内容
                    try:
                        detail_data = initial_state.get('detailInfo', {}).get('data', {})
                        if detail_data:
                            content = detail_data.get('content', '')
                            title = detail_data.get('title', '')
                            summary = detail_data.get('summary', '')
                            
                            if content:
                                # 如果内容是HTML格式，解析提取纯文本
                                if '<' in content and '>' in content:
                                    content_soup = BeautifulSoup(content, 'html.parser')
                                    content = content_soup.get_text(separator='\n')
                                
                                # 组合完整内容
                                full_content = []
                                if title:
                                    full_content.append(f"标题：{title}")
                                if summary:
                                    full_content.append(f"摘要：{summary}")
                                full_content.append("正文：")
                                full_content.append(content)
                                
                                return self._clean_text('\n'.join(full_content))
                    except Exception as e:
                        logging.error(f"提取文章内容失败: {str(e)}")
            
            # 如果网页提取失败，尝试API
            api_url = f"https://www.36kr.com/api/post/{article_id}"
            headers['Accept'] = 'application/json'
            headers['Content-Type'] = 'application/json'
            
            logging.info(f"尝试API获取: {api_url}")
            api_response = session.get(api_url, headers=headers, timeout=30)
            logging.info(f"API状态码: {api_response.status_code}")
            
            if api_response.status_code == 200:
                try:
                    api_data = api_response.json()
                    logging.info("API响应内容前500字符: " + str(api_data)[:500])
                    
                    if 'data' in api_data:
                        content = api_data['data'].get('content', '')
                        title = api_data['data'].get('title', '')
                        summary = api_data['data'].get('summary', '')
                        
                        if content:
                            if '<' in content and '>' in content:
                                content_soup = BeautifulSoup(content, 'html.parser')
                                content = content_soup.get_text(separator='\n')
                            
                            full_content = []
                            if title:
                                full_content.append(f"标题：{title}")
                            if summary:
                                full_content.append(f"摘要：{summary}")
                            full_content.append("正文：")
                            full_content.append(content)
                            
                            return self._clean_text('\n'.join(full_content))
                except Exception as e:
                    logging.error(f"解析API响应失败: {str(e)}")
            
            logging.warning("所有获取内容的方法都失败了")
            return None
            
        except Exception as e:
            logging.error(f"获取36kr内容失败: {str(e)}")
            logging.error("详细错误信息: ", exc_info=True)
            return None 