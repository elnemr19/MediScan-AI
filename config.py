import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '082b3a3551d3ca87'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit
    # Database configuration (if you add user database later)
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///users.db'
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Model paths
    PNEUMONIA_MODEL_PATH = 'models/densenet_pneumonia.h5'
    BRAIN_MODEL_PATH = 'models/Brain tumor classification_edit.h5'
    DRUGS_MODEL_PATH = 'models/CNN_Drugs.h5'
    SENTIMENT_MODEL_PATH = 'models/sentiment_analysis_model.keras'
    TOKENIZER_PATH = 'models/tokenizer.pkl'
    
    # Chatbot settings
    CHATBOT_MODEL = "qwen:1.8b"
    SYSTEM_PROMPT = """
    You are a professional medical chatbot.
    - NEVER include internal thoughts or step-by-step reasoning in responses.
    - NEVER use <think> or explain your thought process.
    - ONLY provide direct answers.
    - Keep responses concise and medically accurate.
    - If the user greets you (e.g., "hi", "hello"), simply greet them back.
    """
    
    
    
