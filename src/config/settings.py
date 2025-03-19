import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.utils.logger import logger


def get_base_path() -> Path:
    """获取项目根目录，兼容 PyInstaller 打包环境"""
    if getattr(sys, '_MEIPASS', None):
        # PyInstaller 打包后的临时资源目录 (_internal)
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent

# 项目根目录（打包时为 _internal，开发时为 src/ 上级）
BASE_DIR = get_base_path()

# 运行时目录（可执行文件所在目录）
RUNTIME_DIR = Path.cwd()

# 配置加载逻辑
def load_config():
    """加载环境配置，按优先级处理 .env 文件"""
    # 1. 优先加载运行时目录下的 .env（如果存在）
    runtime_env = RUNTIME_DIR / ".env"
    if runtime_env.exists():
        load_dotenv(dotenv_path=runtime_env, override=True)
        logger.info(f"Loaded runtime .env from: {runtime_env}")

    # 2. 次优先加载打包的 .env（如果存在）
    bundled_env = BASE_DIR / ".env"
    if bundled_env.exists():
        load_dotenv(dotenv_path=bundled_env, override=False)  # 不覆盖运行时的配置
        logger.info(f"Loaded bundled .env from: {bundled_env}")
    else:
        logger.warning(f"Bundled .env not found at: {bundled_env}")

# 加载配置
load_config()

class Settings:
    """项目配置类"""

    BASE_DIR: Path = BASE_DIR
    MODEL_DIR: str = os.path.join(BASE_DIR, "models")
    MODEL_FILE: str = os.getenv("MODEL_FILE", "onnx_model/model.onnx")
    TOKENIZER_PATH: str = os.getenv("TOKENIZER_PATH", "onnx_model/tokenizer.json")
    GGML_QUIET: bool = os.getenv("GGML_QUIET", "1") == "1"
    LLAMA_VERBOSE: bool = os.getenv("LLAMA_VERBOSE", "0") == "1"
    LLAMA_CTX_SIZE: int = int(os.getenv("LLAMA_CTX_SIZE", "512"))

    def getModelPath(self) -> str:
        return os.path.join(self.MODEL_DIR, self.MODEL_FILE)

    def getTokenizerPath(self) -> str:
        return os.path.join(self.MODEL_DIR, self.TOKENIZER_PATH)

    def log_config(self) -> None:
        """打印当前配置"""
        config_info = (
            "Current Settings:\n"
            f"  BASE_DIR: {self.BASE_DIR}\n"
            f"  MODEL_DIR: {self.MODEL_DIR}\n"
            f"  MODEL_FILE: {self.MODEL_FILE}\n"
            f"  MODEL_PATH: {self.getModelPath()}\n"
            f"  TOKENIZER_PATH: {self.getTokenizerPath()}\n"
            f"  GGML_QUIET: {self.GGML_QUIET}\n"
            f"  LLAMA_VERBOSE: {self.LLAMA_VERBOSE}\n"
            f"  LLAMA_CTX_SIZE: {self.LLAMA_CTX_SIZE}"
        )
        logger.info(config_info)

# 单例配置实例
settings = Settings()
settings.log_config()