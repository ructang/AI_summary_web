from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO
import os
from main import ContentSummarizer, process_content
import logging
from config import settings
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery.result import AsyncResult

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

summarizer = ContentSummarizer()

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="fixed-window"
)

def init_app():
    """初始化应用"""
    # 创建必要的目录
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    os.makedirs(settings.TEMP_DIR, exist_ok=True)

@app.before_request
def validate_request():
    # 添加请求验证逻辑
    pass

@app.route('/')
def index():
    return render_template('index.html',
                         system_name=settings.SYSTEM_NAME,
                         system_description=settings.SYSTEM_DESCRIPTION,
                         version=settings.VERSION)

@app.route('/process', methods=['POST'])
def process_url():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': '请输入URL'}), 400
        
        logging.info(f"收到处理请求，URL: {url}")
        task = process_content.delay(url)  # 使用Celery异步处理
        logging.info(f"创建任务成功，task_id: {task.id}")
        return jsonify({'task_id': task.id}), 202
    except Exception as e:
        logging.error(f"处理请求失败: {str(e)}", exc_info=True)
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/download')
def download():
    file_path = os.path.join(settings.OUTPUT_DIR, 'summary.txt')
    if os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            download_name='summary.txt',
            mimetype='text/plain'
        )
    return jsonify({'error': '文件不存在'}), 404

@app.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    try:
        task = AsyncResult(task_id)
        logging.info(f"查询任务状态: {task_id}, 状态: {task.state}")
        
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': '任务等待中...'
            }
        elif task.state == 'PROGRESS':
            response = {
                'state': task.state,
                'status': task.info.get('message', '处理中...')
            }
        elif task.state == 'SUCCESS':
            result = task.get()
            logging.info(f"任务完成，结果: {result}")
            response = {
                'state': task.state,
                'result': result
            }
        else:
            # 处理失败状态
            error_info = str(task.info) if task.info else '未知错误'
            logging.error(f"任务执行失败: {error_info}")
            response = {
                'state': task.state,
                'status': f'处理失败: {error_info}'
            }
        return jsonify(response)
    except Exception as e:
        logging.error(f"获取任务状态失败: {str(e)}", exc_info=True)
        return jsonify({'error': f'获取任务状态失败: {str(e)}'}), 500

if __name__ == '__main__':
    init_app()
    app.run(debug=True) 