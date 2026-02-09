from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Colab URL'si (başlangıçta boş, sonra güncellenecek)
COLAB_URL = os.environ.get('COLAB_URL', '')

@app.route('/')
def home():
    return jsonify({
        "service": "Colab Video Proxy",
        "status": "running",
        "colab_url": COLAB_URL or "Not set yet",
        "endpoints": {
            "GET /health": "System status",
            "POST /generate": "Create video",
            "POST /update-url": "Update Colab URL"
        }
    })

@app.route('/health')
def health():
    if COLAB_URL:
        try:
            # Colab'a bağlan
            colab_resp = requests.get(f"{COLAB_URL}/health", timeout=5)
            colab_status = colab_resp.json()
        except:
            colab_status = {"error": "Colab unreachable"}
    else:
        colab_status = {"error": "Colab URL not configured"}
    
    return jsonify({
        "proxy": "healthy",
        "colab": colab_status,
        "colab_url": COLAB_URL
    })

@app.route('/generate', methods=['POST'])
def generate():
    if not COLAB_URL:
        return jsonify({"error": "Colab URL not configured"}), 400
    
    try:
        # Colab'a yönlendir
        response = requests.post(
            f"{COLAB_URL}/generate",
            json=request.json,
            timeout=300
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-url', methods=['POST'])
def update_url():
    global COLAB_URL
    COLAB_URL = request.json.get('new_url', '')
    os.environ['COLAB_URL'] = COLAB_URL
    return jsonify({
        "status": "updated",
        "new_url": COLAB_URL,
        "message": "URL updated successfully"
    })

if __name__ == '__main__':
    # DEĞİŞTİR: 5000 → 8080
    port = int(os.environ.get('PORT', 8080))  # BURASI ÖNEMLİ!
    print(f"🚀 Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
