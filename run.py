import sys
import traceback

from src.api.embedding import app
from src.models.model import model_manager
from src.utils.gunicorn_app import StandaloneApplication
from src.utils.logger import logger


# 判断是否为 PyInstaller 打包环境
def is_packaged():
    return getattr(sys, 'frozen', False)


if __name__ == '__main__':
    logger.info("Server start")
    # 初始化模型
    model_manager.initialize()

    if is_packaged():
        logger.info("Starting Gunicorn in packaged mode")
        options = {
            'bind': '0.0.0.0:9999',
            'workers': 1,
            'threads': 4,
            'worker_class': 'gthread',
            'timeout': 60,
            'loglevel': 'debug',
        }
        try:
            logger.info("Attempting to start Gunicorn with options: %s", options)
            gunicorn_app = StandaloneApplication(app, options)
            gunicorn_app.run()
        except Exception as e:
            logger.error(f"Gunicorn failed to start: {str(e)}\n{traceback.format_exc()}")
            sys.exit(1)
        finally:
            logger.info("Main block completed")
    else:
        logger.info("Starting Flask development server")
        app.run(host='0.0.0.0', port=9999, debug=True)
