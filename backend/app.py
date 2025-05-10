from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({"message": "Welcome to Noxheaven!"})
@app.route('/process-choice', methods=['POST'])
def process_choice():
    # Mock response (we'll connect to LLM later)
    data = {
        "new_text": "You chose to host an Evil Ladies event. Ava suggests targeting the Riverfront elite.",
        "new_choices": [
            {"id": 1, "text": "Plan a luxury yacht party"},
            {"id": 2, "text": "Organize a rooftop networking mixer"}
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)