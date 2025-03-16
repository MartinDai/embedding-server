import sys
import traceback

import gunicorn.app.base

from src.api.embedding import app
from src.utils.logger import logger
from src.models.model import model_manager


# 判断是否为 PyInstaller 打包环境
def is_packaged():
    return getattr(sys, 'frozen', False)


# Gunicorn 配置
class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        try:
            super().__init__()
            logger.info("StandaloneApplication initialized")
        except Exception as e:
            logger.error(f"Failed to initialize StandaloneApplication: {str(e)}\n{traceback.format_exc()}")
            raise

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)
        logger.info(f"Gunicorn config loaded with keys: {list(config.keys())}")

    def load(self):
        logger.info("Entering Gunicorn load() method")
        try:
            result = self.application
            logger.info("Application loaded successfully")
            return result
        except Exception as e:
            logger.error(f"Failed to load application: {str(e)}\n{traceback.format_exc()}")
            raise

    def run(self):
        logger.info("Starting Gunicorn run() method")
        try:
            app_instance = self.load()
            logger.info(f"Loaded app instance: {app_instance}")
            super().run()
            logger.info("Gunicorn run() completed")
        except Exception as e:
            logger.error(f"Gunicorn run() failed: {str(e)}\n{traceback.format_exc()}")
            raise
        finally:
            logger.info("Exiting Gunicorn run() method")


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
