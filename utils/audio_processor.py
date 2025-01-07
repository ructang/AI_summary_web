import os
from pytube import YouTube
import speech_recognition as sr
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import logging
from typing import Optional

class AudioProcessor:
    def __init__(self, output_dir: str = "temp_audio"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.recognizer = sr.Recognizer()
        
    def process_url(self, url: str) -> Optional[str]:
        """处理URL中的音频内容"""
        try:
            if "youtube.com" in url or "youtu.be" in url:
                return self._process_youtube(url)
            else:
                return self._process_direct_audio(url)
        except Exception as e:
            logging.error(f"处理音频URL出错: {str(e)}")
            return None
            
    def _process_youtube(self, url: str) -> Optional[str]:
        """处理YouTube视频"""
        try:
            # 下载YouTube视频
            yt = YouTube(url)
            video_path = os.path.join(self.output_dir, "temp_video.mp4")
            audio_path = os.path.join(self.output_dir, "temp_audio.wav")
            
            # 下载音频流
            logging.info("正在下载YouTube视频...")
            yt.streams.filter(only_audio=True).first().download(
                output_path=self.output_dir,
                filename="temp_video.mp4"
            )
            
            # 转换为WAV格式
            logging.info("正在转换音频格式...")
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path)
            video.close()
            
            # 转换为文本
            return self._audio_to_text(audio_path)
        finally:
            # 清理临时文件
            self._cleanup_files([video_path, audio_path])
            
    def _process_direct_audio(self, url: str) -> Optional[str]:
        """处理直接的音频URL"""
        try:
            # 下载音频文件
            response = requests.get(url)
            audio_path = os.path.join(self.output_dir, "temp_audio")
            with open(audio_path, "wb") as f:
                f.write(response.content)
            
            # 检测并转换音频格式
            audio = AudioSegment.from_file(audio_path)
            wav_path = os.path.join(self.output_dir, "temp_audio.wav")
            audio.export(wav_path, format="wav")
            
            # 转换为文本
            return self._audio_to_text(wav_path)
        finally:
            # 清理临时文件
            self._cleanup_files([audio_path, wav_path])
            
    def _audio_to_text(self, audio_path: str) -> Optional[str]:
        """将音频转换为文本"""
        logging.info("正在将音频转换为文本...")
        try:
            with sr.AudioFile(audio_path) as source:
                # 调整识别参数
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.record(source)
                
                # 使用Google Speech Recognition进行识别
                text = self.recognizer.recognize_google(audio, language='zh-CN')
                return text
        except sr.UnknownValueError:
            logging.error("无法识别音频内容")
            return None
        except sr.RequestError as e:
            logging.error(f"语音识别服务出错: {str(e)}")
            return None
            
    def _cleanup_files(self, files: list):
        """清理临时文件"""
        for file in files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                logging.warning(f"清理文件失败 {file}: {str(e)}") 