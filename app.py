from flask import Flask, render_template, request, jsonify
from chatbot.nlp_utils import preprocess_text, detect_intent
from chatbot.response_generator import generate_response
import logging
import os

app = Flask(__name__)

# Basic logging for the Flask app
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def get_bot_response():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON with a 'message' field."}), 400

        payload = request.get_json()
        if 'message' not in payload:
            return jsonify({"error": "Missing 'message' field in request."}), 400

        user_message = payload['message']
        tokens = preprocess_text(user_message)
        intent = detect_intent(user_message)
        reply = generate_response(intent, tokens)
        return jsonify({"reply": reply})

    except Exception as e:
        logger.exception("Unhandled error in /get endpoint")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Respect environment DEBUG flag; default to False for safety
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=debug_mode)
