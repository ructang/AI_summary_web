import os
import sys
import logging
from app import app, socketio, init_app
from config import settings

def print_banner():
    """打印启动横幅"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {settings.SYSTEM_NAME}                                     
║   版本: {settings.VERSION}                                   
║   状态: {'开发模式' if app.debug else '生产模式'}           
║                                                              ║
║   服务已启动:                                               ║
║   - 本地访问: http://127.0.0.1:5000                         ║
║   - 局域网访问: http://本机IP:5000                          ║
║                                                              ║
║   按 Ctrl+C 停止服务                                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_dev():
    """开发环境运行"""
    try:
        print("\n正在启动开发服务器...")
        print("初始化系统组件...")
        init_app()
        print("加载配置完成！")
        
        print_banner()
        
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

def run_prod():
    """生产环境运行"""
    try:
        print("\n正在启动生产服务器...")
        print("初始化系统组件...")
        init_app()
        print("加载配置完成！")
        
        print_banner()
        
        socketio.run(
            app,
            host='0.0.0.0',
            port=int(os.getenv('PORT', 5000)),
            debug=False,
            use_reloader=False,
            log_output=False
        )
    except Exception as e:
        logging.error(f"启动失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'prod':
            run_prod()
        else:
            run_dev()
    except KeyboardInterrupt:
        print("\n\n服务已停止！")
        sys.exit(0) 