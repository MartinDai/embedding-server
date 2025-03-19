from flask import Flask

from src.models.onnx_model_manager import onnx_model_manager


def create_app():
    app = Flask(__name__)

    # 初始化模型
    # gguf_model_manager.initialize()
    onnx_model_manager.initialize()

    # 注册路由
    from src.api.embedding import embedding_bp
    app.register_blueprint(embedding_bp, url_prefix="/")

    return app
