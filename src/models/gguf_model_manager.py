import os
import sys
from typing import Optional

import numpy as np
from llama_cpp import Llama

from src.config.settings import settings
from src.utils.logger import logger

class GgufModelManager:
    def __init__(self):
        self.llm: Optional[Llama] = None
        self.model_path = settings.MODEL_PATH

    def initialize(self):
        """初始化模型"""
        if self.llm is not None:
            logger.info("Model already initialized")
            return

        logger.info(f"Loading GGUF model from: {self.model_path}")
        if not os.path.exists(self.model_path):
            logger.error(f"Model file not found at {self.model_path}")
            sys.exit(1)

        # 处理 GGML 日志输出
        if settings.GGML_QUIET:
            sys.stderr = open(os.devnull if os.name != "nt" else "nul", "w")

        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=settings.LLAMA_CTX_SIZE,
                embedding=True,
                verbose=settings.LLAMA_VERBOSE
            )
            logger.info("GGUF Model loaded successfully")
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
gguf_model_manager = GgufModelManager()
