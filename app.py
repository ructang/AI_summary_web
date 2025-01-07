from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO
import os
from main import ContentSummarizer
import threading
import logging
from config import settings
from werkzeug.serving import WSGIRequestHandler

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='\033[1;36m%(asctime)s\033[0m - \033[1;32m%(levelname)s\033[0m - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 设置Werkzeug日志级别
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.WARNING)

# 设置Socket.IO日志级别
logging.getLogger('socketio').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)

# 创建应用日志记录器
logger = logging.getLogger('tommy_ai')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# 配置Socket.IO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    logger=False,
    engineio_logger=False
)

summarizer = ContentSummarizer()

class ProgressHandler(logging.Handler):
    def emit(self, record):
        socketio.emit('progress', {'message': record.getMessage()})

# 添加自定义处理器到应用日志记录器
logger.addHandler(ProgressHandler())

@app.route('/')
def index():
    logger.info("访问主页")
    return render_template('index.html',
                         system_name=settings.SYSTEM_NAME,
                         system_description=settings.SYSTEM_DESCRIPTION,
                         version=settings.VERSION)

@app.route('/process', methods=['POST'])
def process_url():
    url = request.json.get('url')
    if not url:
        logger.warning("收到空URL请求")
        return jsonify({'error': '请输入URL'}), 400
    
    logger.info(f"开始处理URL: {url}")
    
    def process():
        try:
            summarizer.process_url(url)
            logger.info("处理完成")
            socketio.emit('complete', {
                'status': 'success',
                'message': '处理完成！'
            })
        except Exception as e:
            logger.error(f"处理失败: {str(e)}")
            socketio.emit('complete', {
                'status': 'error',
                'message': f'处理失败: {str(e)}'
            })
    
    thread = threading.Thread(target=process)
    thread.daemon = True
    thread.start()
    return jsonify({'message': '开始处理'})

@app.route('/download')
def download():
    file_path = os.path.join(settings.OUTPUT_DIR, 'summary.txt')
    if os.path.exists(file_path):
        logger.info("下载摘要文件")
        return send_file(
            file_path,
            as_attachment=True,
            download_name='summary.txt',
            mimetype='text/plain'
        )
    logger.warning("请求下载不存在的文件")
    return jsonify({'error': '文件不存在'}), 404

@app.route('/particles.json')
def particles_config():
    return send_file('static/particles.json')

@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404错误: {request.url}")
    return jsonify({'error': '页面不存在'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"500错误: {str(e)}")
    return jsonify({'error': '服务器内部错误'}), 500

def init_app():
    """初始化应用"""
    logger.info("初始化应用...")
    
    # 确保必要的目录存在
    for directory in [settings.OUTPUT_DIR, settings.TEMP_DIR]:
        if not os.path.exists(directory):
            logger.info(f"创建目录: {directory}")
            os.makedirs(directory)
    
    # 设置请求处理器
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    
    logger.info("应用初始化完成")

if __name__ == '__main__':
    init_app()
    # 使用gevent作为异步后端
    socketio.run(
        app,
        host='127.0.0.1',
        port=5000,
        debug=False,  # 生产环境关闭debug模式
        use_reloader=False,  # 关闭重载器
        log_output=False  # 关闭Socket.IO日志
    ) 