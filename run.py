import os
import sys
import logging
from app import app, socketio, init_app

if __name__ == '__main__':
    try:
        print("\n正在启动开发服务器...")
        print("初始化系统组件...")
        init_app()
        print("加载配置完成！")
        
        socketio.run(
            app,
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except Exception as e:
        logging.error(f"启动失败: {str(e)}")
        sys.exit(1) 