import traceback

import gunicorn.app.base

from src.utils.logger import logger


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
