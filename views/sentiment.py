from flask import Blueprint, render_template, request, flash
from flask_login import login_required
import subprocess
import logging
from datetime import datetime

# Initialize blueprint
sentiment_bp = Blueprint('sentiment', __name__)
logger = logging.getLogger(__name__)

@sentiment_bp.route('/', methods=['GET', 'POST'])
@login_required
def sentiment():
    if request.method == 'POST':
        try:
            text = request.form.get('text', '').strip()
            
            # Input validation
            if not text or len(text) < 10:
                raise ValueError("Please enter valid text (10-1000 chars)")
            
            # Call the isolated predictor
            result = subprocess.run(
                ['python', 'isolated_predictor.py', text],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse output (last line contains the score)
            raw_score = float(result.stdout.strip().split('\n')[-1])
            
            response = {
                'sentiment': "Positive" if raw_score > 0.5 else "Negative",
                'confidence': raw_score if raw_score > 0.5 else 1 - raw_score,
                'raw_score': raw_score
            }
            
            logger.info(f"Prediction result: {response}")
            return render_template('sentiment.html',
                               result=response,
                               text=text,
                               now=datetime.now())
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Prediction failed: {e.stderr}")
            flash("Prediction service unavailable", 'error')
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            flash(str(e), 'error')
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            flash("An unexpected error occurred", 'error')
    
    return render_template('sentiment.html', now=datetime.now())
@sentiment_bp.context_processor
def inject_sentiment_labels():
    return {
        'sentiment_labels': {
            'Positive': 'success',
            'Negative': 'danger',
            'Neutral': 'info'
        }
    }