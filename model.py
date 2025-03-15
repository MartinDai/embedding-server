import os
import sys

import numpy as np
from llama_cpp import Llama

from logger import logger

# 检查环境变量控制 GGML 日志
GGML_QUIET = os.getenv('GGML_QUIET', '1') == '1'
if GGML_QUIET:
    sys.stderr = open(os.devnull if os.name != 'nt' else 'nul', 'w')


class ModelManager:
    def __init__(self):
        self.llm = None
        self.model_path = self._get_model_path()
        self.verbose = os.getenv('LLAMA_VERBOSE', '0') == '1'

    def _get_model_path(self):
        """动态获取模型路径，兼容 PyInstaller 打包"""
        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        return os.path.join(base_path, 'models', 'embedding.gguf')

    def initialize(self):
        """初始化模型"""
        if self.llm is None:
            logger.info(f"Model path: {self.model_path}")
            if not os.path.exists(self.model_path):
                logger.error(f"Model file not found at {self.model_path}")
                sys.exit(1)
            logger.info("Loading model...")
            try:
                self.llm = Llama(model_path=self.model_path, n_ctx=512, embedding=True, verbose=self.verbose)
                logger.info("Model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}")
                sys.exit(1)

    def get_embedding(self, text):
        """生成文本的嵌入"""
        if self.llm is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        try:
            embedding = self.llm.embed(text)
            return np.array(embedding).tolist()
        except Exception as e:
            logger.error(f"Embedding error: {str(e)}")
            raise


# 单例实例
model_manager = ModelManager()
