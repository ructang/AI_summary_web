# Tommy的人工智能知识大脑

一个基于 DeepSeek 大模型的智能内容处理系统，支持网页内容和音频内容的自动摘要生成。

## 功能特点

- 🌐 支持网页内容处理
- 🎵 支持音频内容处理（包括YouTube视频）
- 🤖 使用 DeepSeek 大模型生成摘要
- 📊 实时处理进度显示
- 💻 现代化Web界面
- 🎨 粒子动画背景

## 技术栈

- Python 3.8+
- Flask + Socket.IO
- DeepSeek API
- Bootstrap 5
- Particle.js

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

3. 配置环境变量：
创建 `.env` 文件并添加：
```
DEEPSEEK_API_KEY=你的API密钥
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
2. 在输入框中输入网页URL或音频URL
3. 点击"开始处理"按钮
4. 等待处理完成
5. 下载生成的摘要文件

## 目录结构

```
├── app.py              # Flask应用主文件
├── config.py           # 配置文件
├── main.py            # 主要处理逻辑
├── requirements.txt    # 项目依赖
├── run.py             # 启动脚本
├── static/            # 静态文件
│   ├── images/        # 图片资源
│   ├── style.css      # 样式文件
│   ├── script.js      # 客户端脚本
│   └── particles.json # 粒子效果配置
├── templates/         # 模板文件
│   └── index.html    # 主页面
└── utils/            # 工具类
    ├── audio_processor.py    # 音频处理
    ├── content_fetcher.py    # 内容获取
    ├── deepseek_client.py    # API客户端
    └── text_splitter.py      # 文本分割
```

## 注意事项

- 需要有效的 DeepSeek API 密钥
- 音频处理需要安装相关系统依赖
- 建议在虚拟环境中运行

## 许可证

MIT License