from flask import request, jsonify, Blueprint

from src.models.onnx_model_manager import onnx_model_manager
from src.utils.logger import logger

embedding_bp = Blueprint("embedding", __name__)

@embedding_bp.route('/embedding', methods=['POST'])
def embedding_endpoint():
    try:
        data = request.get_json()
        texts = data.get('text')
        if not texts:
            return jsonify({'error': 'Missing text parameter'}), 400
        if isinstance(texts, str):
            texts = [texts]

        embeddings = [onnx_model_manager.get_embedding(text) for text in texts]
        logger.info(f"Generated embeddings for {len(texts)} texts")
        return jsonify({
            'status': 'success',
            'embeddings': embeddings,
            'dimension': len(embeddings[0])
        })
    except Exception as e:
        logger.error(f"Error in endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500
