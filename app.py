from flask import Flask, render_template, request, jsonify
import main
import datetime

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
    translated_text = main.translate(text, input_language, target_language)
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5001) # Change this line



