from flask import Flask, render_template, request, jsonify, escape
import main
import datetime
from main import generate_summary
from main import detect_language 
import json



app = Flask(__name__)
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['text']
    input_language = data['input_language']
    target_language = data['target_language']
    api_key = data['api_key']  # Add this line
 # Add this line
    translated_text = main.translate(text, input_language, target_language, api_key)  # Pass the API key here
    conversation_history.append((text, translated_text))
    return jsonify({'translated_text': translated_text})



@app.route('/save-conversation', methods=['POST'])
def save_conversation():
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    with open(filename, "w") as f:
        for original_text, translated_text in conversation_history:
            f.write("Original Text:\n" + original_text + "\n")
            f.write("Translated Text:\n" + translated_text + "\n")
            f.write("\n")
    conversation_history.clear()
    return jsonify({'filename': filename})

@app.route('/summarize-conversation', methods=['POST'])
def summarize_conversation():
    api_key = request.json['api_key']
    summary_original = main.generate_summary('\n'.join([conv[0] for conv in json.loads(request.json['conversation'])]), api_key=api_key)

    summary_translated = main.translate(summary_original, main.detect_language(summary_original), request.json['target_language'], api_key)
    return jsonify({'summary': {'original': summary_original, 'translated': summary_translated}})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5001) # Change this line



