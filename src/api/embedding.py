from flask import Flask, request, jsonify

from src.utils.logger import logger
from src.models.model import model_manager

app = Flask(__name__)

@app.route('/embedding', methods=['POST'])
def embedding_endpoint():
    try:
        data = request.get_json()
        texts = data.get('text')
        if not texts:
            return jsonify({'error': 'Missing text parameter'}), 400
        if isinstance(texts, str):
            texts = [texts]

        embeddings = [model_manager.get_embedding(text) for text in texts]
        logger.info(f"Generated embeddings for {len(texts)} texts")
        return jsonify({
            'status': 'success',
            'embeddings': embeddings,
            'dimension': len(embeddings[0])
        })
    except Exception as e:
        logger.error(f"Error in endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500
