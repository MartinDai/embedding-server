from flask import Flask, request, jsonify
from llama_cpp import Llama
import logging
import os
import numpy as np

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 加载 GGUF 模型
model_path = os.path.join(os.path.dirname(__file__), 'models', 'conan-embedding-v1-q4_k_m.gguf')
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model path {model_path} does not exist!")

# 初始化模型
# n_ctx 是上下文长度，embedding=True 表示启用 embedding 模式
llm = Llama(model_path=model_path, n_ctx=512, embedding=True)

def get_embedding(text):
    """生成文本的 embedding"""
    # 使用 llama.cpp 生成 embedding
    embedding = llm.embed(text)
    return np.array(embedding).tolist()

@app.route('/embedding', methods=['POST'])
def embedding_endpoint():
    try:
        data = request.get_json()
        texts = data.get('text')
        if not texts:
            return jsonify({'error': 'Missing text parameter'}), 400

        if isinstance(texts, str):
            texts = [texts]

        # 批量生成 embeddings
        embeddings = [get_embedding(text) for text in texts]

        return jsonify({
            'status': 'success',
            'embeddings': embeddings,
            'dimension': len(embeddings[0])
        })
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)