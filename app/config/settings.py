import os
from pathlib import Path

from dotenv import load_dotenv

from app.utils.logger import logger

# 运行时目录
RUNTIME_DIR = Path.cwd()


# 配置加载逻辑
def load_config():
    """加载环境配置 .env 文件"""
    runtime_env = RUNTIME_DIR / ".env"
    if runtime_env.exists():
        load_dotenv(dotenv_path=runtime_env, override=True)
        logger.info(f"Loaded runtime .env from: {runtime_env}")


# 加载配置
load_config()


class Settings:
    """项目配置类"""
    MODEL_DIR: str = os.path.join(RUNTIME_DIR, "models")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "onnx/model.onnx")
    TOKENIZER_PATH: str = os.getenv("TOKENIZER_PATH", "onnx/tokenizer.json")

    def getModelPath(self) -> str:
        return os.path.join(self.MODEL_DIR, self.MODEL_PATH)

    def getTokenizerPath(self) -> str:
        return os.path.join(self.MODEL_DIR, self.TOKENIZER_PATH)

    def log_config(self) -> None:
        """打印当前配置"""
        config_info = (
            "Current Settings:\n"
            f"  RUNTIME_DIR: {RUNTIME_DIR}\n"
            f"  MODEL_DIR: {self.MODEL_DIR}\n"
            f"  MODEL_PATH: {self.getModelPath()}\n"
            f"  TOKENIZER_PATH: {self.getTokenizerPath()}\n"
        )
        logger.info(config_info)


# 单例配置实例
settings = Settings()
settings.log_config()
