from flask import Flask, request, jsonify
from googletrans import Translator
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)  # allow frontend requests

translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()

        # Text translation
        text = data.get('text', '')
        target_lang = data.get('target_lang') or data.get('target') or 'en'

        if text:
            translated = translator.translate(text, dest=target_lang)
            return jsonify({
                "source_language": translated.src,
                "target_language": target_lang,
                "translated_text": translated.text
            }), 200

        # Text file upload
        if 'file_base64' in data:
            file_content = base64.b64decode(data['file_base64']).decode('utf-8')
            translated = translator.translate(file_content, dest=target_lang)
            return jsonify({
                "original_file_text": file_content,
                "translated_text": translated.text
            }), 200

        # Image upload placeholder
        if 'image_base64' in data:
            extracted_text = "Placeholder text from image"
            translated = translator.translate(extracted_text, dest=target_lang)
            return jsonify({
                "extracted_text": extracted_text,
                "translated_text": translated.text
            }), 200

        return jsonify({"error": "No text or file provided"}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Translation API running"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
