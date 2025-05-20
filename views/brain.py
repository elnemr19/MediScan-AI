from flask import Blueprint, render_template, request, flash, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os
import logging
from utils.model_utils import load_brain_model, predict_brain_tumor
from config import Config
from datetime import datetime

brain_bp = Blueprint('brain', __name__)
model = load_brain_model(Config.BRAIN_MODEL_PATH)
logger = logging.getLogger(__name__)

@brain_bp.route('/brain', methods=['GET', 'POST'])
def brain():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                raise ValueError("No file selected")
                
            file = request.files['file']
            if file.filename == '':
                raise ValueError("Please select an MRI scan")
            
            # Generate secure filename
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"brain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
            filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save and process
            file.save(filepath)
            with Image.open(filepath) as img:
                result = predict_brain_tumor(model, img)
            
            return render_template('brain.html',
                               result=result,
                               image_url=url_for('static', 
                                               filename=f'uploads/{unique_filename}',
                                               _external=True),
                               now=datetime.now())
                               
        except Exception as e:
            logger.error(f"Brain tumor detection error: {str(e)}")
            flash(f"Error processing MRI scan: {str(e)}", 'error')
    
    return render_template('brain.html', now=datetime.now())