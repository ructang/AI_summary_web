# Tommy的人工智能知识大脑

一个基于 DeepSeek 大模型的智能内容处理系统，支持网页内容和音频内容的自动摘要生成。

## 功能特点

- 🌐 支持网页内容处理
  - 自动提取网页正文
  - 智能分块处理长文本
  - 保持原文重要信息
- 🎵 支持音频内容处理
  - YouTube视频音频提取
  - 常见音频格式支持（mp3, wav等）
  - 中文语音识别转文字
- 🤖 智能摘要生成
  - 结构化信息提取
  - 多级标题组织
  - 重要数据保留
  - 逻辑关系梳理
- 📊 用户友好界面
  - 实时处理进度展示
  - 优雅的粒子动画背景
  - 响应式设计适配
  - 便捷的结果下载

## 技术栈

### 后端
- Python 3.8+
- Flask + Flask-SocketIO
- DeepSeek Chat API
- speech_recognition
- pytube
- pydub
- moviepy

### 前端
- Bootstrap 5
- Particles.js
- Socket.IO
- Font Awesome
- Animate.css

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/ructang/AI_summary.git
cd AI_summary
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置文件：
创建 `config.py` 文件并配置：
```python
DEEPSEEK_API_KEY = "你的API密钥"
SYSTEM_NAME = "系统名称"
SYSTEM_DESCRIPTION = "系统描述"
VERSION = "版本号"
OUTPUT_DIR = "输出目录"
CHUNK_SIZE = 2000  # 文本分块大小
```

## 运行

### 开发环境
```bash
python run.py
```

### 生产环境
```bash
python run.py prod
```

## 使用方法

1. 启动服务后访问 http://localhost:5000
2. 在输入框中输入以下任一类型的URL：
   - 网页链接
   - YouTube视频链接
   - 音频文件链接
3. 点击"开始处理"按钮
4. 实时查看处理进度
5. 处理完成后下载摘要文件

## 目录结构

```
├── app.py              # Flask应用主文件
├── config.py           # 配置文件
├── main.py            # 核心处理逻辑
├── run.py             # 启动脚本
├── static/            # 静态资源
│   ├── images/        # 图片资源
│   ├── style.css      # 样式文件
│   ├── script.js      # 客户端脚本
│   └── particles.json # 粒子效果配置
├── templates/         # HTML模板
│   └── index.html    # 主页面
└── utils/            # 工具类
    ├── audio_processor.py    # 音频处理
    ├── content_fetcher.py    # 内容获取
    ├── deepseek_client.py    # AI接口
    └── text_splitter.py      # 文本分割
```

## 系统要求

- Python 3.8+
- 足够的系统内存（建议4GB以上）
- 稳定的网络连接
- 有效的 DeepSeek API 密钥

## 注意事项

- 音频处理需要安装系统依赖：
  - ffmpeg（音频转换）
  - portaudio（音频处理）
- 建议在虚拟环境中运行
- YouTube视频下载需要科学上网
- 处理大文件时需要较长时间

## 许可证

MIT License

## 作者

Tommy

## 问题反馈

如有问题或建议，请提交Issue或Pull Request