import os
import sys
from typing import Optional

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

from app.config.settings import settings
from app.utils.logger import logger

class OnnxModelManager:
    def __init__(self):
        self.session: Optional[ort.InferenceSession] = None
        self.tokenizer = None
        # 设置 ONNX 模型路径
        self.model_path = settings.getModelPath()
        # 如果你的模型文件夹中还有单独的 tokenizer 文件夹或配置文件，可以相应调整
        self.tokenizer_path = settings.getTokenizerPath()

    def initialize(self):
        """初始化模型"""
        if self.session is not None:
            logger.info("Model already initialized")
            return

        logger.info(f"Loading ONNX model from: {self.model_path}")
        if not os.path.exists(self.model_path):
            logger.error(f"Model file not found at {self.model_path}")
            sys.exit(1)

        try:
            # 创建会话选项
            session_options = ort.SessionOptions()
            # 动态获取 CPU 核心数并设置线程数
            cpu_count = os.cpu_count() or 4  # 如果获取失败，默认使用 4
            session_options.intra_op_num_threads = cpu_count
            session_options.inter_op_num_threads = 1
            session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL  # 启用所有优化

            # 加载 ONNX 模型
            self.session = ort.InferenceSession(
                self.model_path,
                sess_options=session_options,  # 传入会话选项
                providers=['CPUExecutionProvider']
            )
            # 加载 tokenizer 并启用截断
            self.tokenizer = Tokenizer.from_file(self.tokenizer_path)
            self.tokenizer.enable_truncation(max_length=512)  # 设置最大长度为 512
            logger.info("ONNX Model and tokenizer loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            sys.exit(1)

    def get_embedding(self, text):
        """生成文本的嵌入"""
        if self.session is None or self.tokenizer is None:
            raise RuntimeError("Model not initialized. Call initialize() first.")

        try:
            # 使用 tokenizers 进行编码
            encoding = self.tokenizer.encode(text)
            input_ids = np.array([encoding.ids], dtype=np.int64)  # [1, seq_len]
            attention_mask = np.array([encoding.attention_mask], dtype=np.int64)

            input_feed = {
                "input_ids": input_ids,
                "attention_mask": attention_mask
            }

            outputs = self.session.run(None, input_feed)
            embedding = outputs[0][0, 0]  # 取 [CLS] token
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Embedding error: {str(e)}")
            raise


# 单例实例
model_manager = OnnxModelManager()
