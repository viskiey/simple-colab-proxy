from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
COLAB_URL = os.environ.get('COLAB_URL', '')

@app.route('/')
def home():
    return jsonify({"service": "Video Proxy", "status": "running"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "colab_url": COLAB_URL})

@app.route('/generate', methods=['POST'])
def generate():
    if not COLAB_URL:
        return jsonify({"error": "Colab URL not set"}), 400
    try:
        resp = requests.post(f"{COLAB_URL}/generate", json=request.json, timeout=300)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-url', methods=['POST'])
def update_url():
    global COLAB_URL
    COLAB_URL = request.json.get('new_url', '')
    os.environ['COLAB_URL'] = COLAB_URL
    return jsonify({"status": "updated", "new_url": COLAB_URL})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
