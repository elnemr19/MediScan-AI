from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import ollama
from config import Config

chatbot_bp = Blueprint('chatbot', __name__)

SYSTEM_PROMPT = Config.SYSTEM_PROMPT

@chatbot_bp.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    if request.method == 'POST':
        user_input = request.json.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400
        
        try:
            # Prepare messages with system prompt
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
            
            # Get response from Qwen model
            response = ollama.chat(
                model=Config.CHATBOT_MODEL,
                messages=messages
            )
            
            return jsonify({
                'response': response['message']['content']
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('chatbot.html')