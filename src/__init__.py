from flask import Flask

from src.models.model import model_manager


def create_app():
    app = Flask(__name__)

    # 初始化模型
    model_manager.initialize()

    # 注册路由
    from src.api.embedding import embedding_bp
    app.register_blueprint(embedding_bp, url_prefix="/")

    return app
