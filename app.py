from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO
import os
from main import ContentSummarizer
import logging
from config import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

summarizer = ContentSummarizer()

@app.route('/')
def index():
    return render_template('index.html',
                         system_name=settings.SYSTEM_NAME,
                         system_description=settings.SYSTEM_DESCRIPTION,
                         version=settings.VERSION)

@app.route('/process', methods=['POST'])
def process_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': '请输入URL'}), 400
    
    try:
        result = summarizer.process_url(url)
        return jsonify({'message': '处理完成', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

if __name__ == '__main__':
    app.run(debug=True) 