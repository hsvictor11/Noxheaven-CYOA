from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import logging
import re
from game_state import GameStateManager
from database import DatabaseManager

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)

@app.route('/save', methods=['POST'])
def save_game():
    data = request.json
    save_id = GameStateManager.create_save(
        player_name=data['player_name'],
        initial_state=data['game_state']
    )
    return jsonify({"save_id": save_id})

@app.route('/load/<int:save_id>', methods=['GET'])
def load_game(save_id):
        return jsonify(GameStateManager.get_save(save_id))

@app.route('/history/<int:save_id>', methods=['GET'])
def get_history(save_id):
    return jsonify(GameStateManager.get_recent_history(save_id))

@app.route('/saves/<int:save_id>', methods=['GET'])
def get_save_endpoint(save_id):
    save_data = GameStateManager.get_save(save_id)
    if save_data:
        # Convert JSON string to dict
        save_data['game_state'] = json.loads(save_data['game_state'])
        return jsonify(save_data)
    else:
        return jsonify({"error": "Save not found"}), 404

@app.route('/test')
def test():
    return jsonify({"message": "Flask is running!"})

# KoboldCpp API settings
KOBOLD_API_URL = "http://localhost:5001/api/v1/generate"

current_state = {
    "location": "Marcus' Penthouse",
    "reputation": "Low",
    "obsidian_progress": 0
}

def generate_with_kobold(prompt):
    try:
        # Define the payload here
        payload = {
            "prompt": prompt,
            "max_length": 200,
            "temperature": 0.7,
            "stop_sequence": ["</end>"]
        }
        response = requests.post(KOBOLD_API_URL, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()["results"][0]["text"].strip()
    except Exception as e:
        app.logger.error(f"KoboldCpp Error: {e}")
        raise

@app.route('/process-choice', methods=['POST'])
def process_choice():
    try:
        data = request.json
        choice_id = data.get('choiceId')

        prompt = f"""<s>[INST]
        **Strict Rules**:
        - Write [TEXT] and [CHOICES] in uppercase.
        - Do NOT use markdown or special characters.
        - Follow the example format exactly.
        You are the narrator for Noxheaven, a dark CYOA game. Follow these rules strictly:
        1. Generate a 2-3 sentence narrative under [TEXT].
        2. List 2-3 choices under [CHOICES], numbered as 1., 2., etc.

        Current State: {current_state}
        Player Choice: {choice_id}

        Example Response:
        [TEXT] You decide to host an Evil Ladies event. Ava suggests targeting the Riverfront elite, but warns that their connections are shaky. [/TEXT]
        [CHOICES]
        1. Plan a luxury yacht party to impress the elite.
        2. Organize a discreet meeting at The Underground instead.
        [/CHOICES]

        Now generate the response for the current scenario:
        [/INST]
        """

        llm_response = generate_with_kobold(prompt)

        # Inside the process_choice() function:
        try:
            # Extract [TEXT] content (ignore closing tags)
            text_section = llm_response.split("[TEXT]")[1].split("[/TEXT]")[0].strip()
            text = text_section.split("[CHOICES]")[0].strip()  # Handle nested splits

            # Extract choices (flexible numbering)
            choices_section = llm_response.split("[CHOICES]")[1].strip()
            choices = []
            for line in choices_section.split("\n"):
                line = line.strip()
                if line and line[0].isdigit():
                    # Split on ". " or ") " or other delimiters
                    choice_text = re.split(r'\.\s+|\]\s+', line, 1)[-1].strip()
                    choices.append({"id": len(choices)+1, "text": choice_text})

            return jsonify({"new_text": text, "new_choices": choices})

        except Exception as e:
            return jsonify({"error": f"Parsing failed: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Add this block