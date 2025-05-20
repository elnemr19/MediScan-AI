from flask import Blueprint, render_template, request, flash, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os
import logging
from utils.model_utils import load_drugs_model, predict_drug_class
from config import Config
from datetime import datetime

drugs_bp = Blueprint('drugs', __name__)
model = load_drugs_model(Config.DRUGS_MODEL_PATH)
logger = logging.getLogger(__name__)

@drugs_bp.route('/drugs', methods=['GET', 'POST'])
def drugs():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                raise ValueError("No file selected")
                
            file = request.files['file']
            if file.filename == '':
                raise ValueError("Please select a drug image")
            
            # Generate secure filename
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"drug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
            filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save and process
            file.save(filepath)
            with Image.open(filepath) as img:
                result = predict_drug_class(model, img)
            
            return render_template('drugs.html',
                               result=result,
                               image_url=url_for('static', 
                                               filename=f'uploads/{unique_filename}',
                                               _external=True),
                               now=datetime.now())
                               
        except Exception as e:
            logger.error(f"Drug classification error: {str(e)}")
            flash(f"Error processing drug image: {str(e)}", 'error')
    
    return render_template('drugs.html', now=datetime.now())