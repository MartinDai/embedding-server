from flask import Flask

from app.model.onnx_model_manager import model_manager

app = Flask(__name__)

# 初始化模型
model_manager.initialize()

# 注册路由
from app.api.embedding import embedding_bp
app.register_blueprint(embedding_bp, url_prefix="/")