from app import app, test_connections
from flask import jsonify

@app.route("/test-api-keys")
def test_api_keys():
    """Test all API key configurations"""
    try:
        # Test API key presence
        from app import HUGGINGFACE_API_KEY, ANTHROPIC_API_KEY, COHERE_API_KEY
        
        status = {
            "huggingface": {
                "present": bool(HUGGINGFACE_API_KEY),
                "key_starts_with": HUGGINGFACE_API_KEY[:4] + "..." if HUGGINGFACE_API_KEY else None
            },
            "anthropic": {
                "present": bool(ANTHROPIC_API_KEY),
                "key_starts_with": ANTHROPIC_API_KEY[:4] + "..." if ANTHROPIC_API_KEY else None
            },
            "cohere": {
                "present": bool(COHERE_API_KEY),
                "key_starts_with": COHERE_API_KEY[:4] + "..." if COHERE_API_KEY else None
            }
        }
        
        # Test model connections
        model_results = test_connections()
        
        return jsonify({
            "api_key_status": status,
            "model_test_results": model_results.json
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "Configuration error"
        }), 500

if __name__ == "__main__":
    app.run(debug=True) 