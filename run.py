import sys
import traceback

from gunicorn.app.base import BaseApplication

from app.main import app
from app.utils.logger import logger


class GunicornApp(BaseApplication):
    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load_config(self):
        # 应用传入的配置选项
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        # 返回 WSGI 应用
        return self.application


if __name__ == '__main__':
    logger.info("Starting Embedding Server")

    options = {
        'bind': '0.0.0.0:8080',
        'workers': 1,
        'threads': 4,
        'worker_class': 'gthread',
        'timeout': 60,
        'loglevel': 'info',
    }
    try:
        logger.info("Attempting to start Gunicorn with options: %s", options)
        gunicorn_app = GunicornApp(app, options)
        gunicorn_app.run()
    except Exception as e:
        logger.error(f"Gunicorn failed to start: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1)
    finally:
        logger.info("Main block completed")
