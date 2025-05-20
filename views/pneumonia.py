from flask import Blueprint, render_template, request, flash, url_for
from utils.model_utils import load_pneumonia_model, predict_pneumonia
from utils.file_utils import save_uploaded_file
from config import Config
from PIL import Image
import logging
import os
from datetime import datetime

pneumonia_bp = Blueprint('pneumonia', __name__)
model = load_pneumonia_model(Config.PNEUMONIA_MODEL_PATH)
logger = logging.getLogger(__name__)

@pneumonia_bp.route('/pneumonia', methods=['GET', 'POST'])
def pneumonia():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                raise ValueError("No file part")
                
            file = request.files['file']
            if file.filename == '':
                raise ValueError("No selected file")
            
            # Save file with validation
            filename, filepath = save_uploaded_file(file)
            
            # Process image
            with Image.open(filepath) as img:
                result = predict_pneumonia(model, img)
            
            # Generate proper URL
            image_url = url_for(
                'static', 
                filename=f'uploads/{filename}',
                _external=True
            )
            
            return render_template(
                'pneumonia.html',
                result=result,
                image_url=image_url,
                now=datetime.now()  # For cache busting
            )
                               
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            flash(str(e), 'error')
    
    return render_template('pneumonia.html', now=datetime.now())