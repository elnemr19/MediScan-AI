import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from PIL import Image
import pickle
import joblib
import os

tf.config.set_visible_devices([], 'GPU')  # Disable GPU
tf.get_logger().setLevel('ERROR')

def load_pneumonia_model(model_path):
    return tf.keras.models.load_model(model_path)

def load_brain_model(model_path):
    return tf.keras.models.load_model(model_path)

# Global model and tokenizer instances
_sentiment_model = None
_sentiment_tokenizer = None

def load_sentiment_model(model_path, tokenizer_path):
    # Disable oneDNN optimizations
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    
    model = tf.keras.models.load_model(
        model_path,
        compile=False
    )
    # Force immediate initialization
    model.predict(np.zeros((1, 300)))  # Match your input shape
    
    with open(tokenizer_path, 'rb') as f:
        tokenizer = pickle.load(f)
    
    return model, tokenizer

def predict_pneumonia(model, img, img_size=224):
    try:
        # Convert to RGB if image is grayscale
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = img.resize((img_size, img_size))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        prediction = model.predict(img_array)[0][0]
        return "Pneumonia" if prediction > 0.5 else "Normal"
        
    except Exception as e:
        raise ValueError(f"Image processing failed: {str(e)}")



def predict_brain_tumor(model, img, img_size=224):
    try:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # High-quality resizing
        img = img.resize((img_size, img_size), Image.Resampling.LANCZOS)
        
        # Normalize and preprocess
        img_array = np.array(img, dtype=np.float32) 
        img_array = np.expand_dims(img_array, axis=0)
        
        # Get predictions
        predictions = model.predict(img_array, verbose=0)[0]
        class_names = ['brain_glioma', 'brain_menin', 'brain_tumor']
        
        # Debug output
        print("Prediction scores:", {k:v for k,v in zip(class_names, predictions)})
        
        return class_names[np.argmax(predictions)]
        
    except Exception as e:
        raise ValueError(f"Brain tumor prediction failed: {str(e)}")


def load_drugs_model(model_path):
    """Load the pharmaceutical drugs classification model"""
    model = tf.keras.models.load_model(model_path)
    # Force immediate initialization
    model.predict(np.zeros((1, 100, 100, 3)))  # Match your input shape
    return model

def predict_drug_class(model, img, img_size=100):
    """Predict the class of a pharmaceutical drug from its image"""
    try:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = img.resize((img_size, img_size))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        predictions = model.predict(img_array)[0]
        class_names = ['Alaxan', 'Bactidol', 'Bioflu', 'Biogesic', 'DayZinc', 'Decolgen', 'Fish Oil', 'Kremil S', 'Medicol', 'Neozep'] 
        return class_names[np.argmax(predictions)]
        
    except Exception as e:
        raise ValueError(f"Drug classification failed: {str(e)}")






def predict_sentiment(model, tokenizer, text, max_length=300):
    try:
        # Convert to exact numpy float32
        sequence = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequence, maxlen=max_length).astype('float32')
        
        # Critical: Use this exact prediction call
        with tf.device('/CPU:0'):
            prediction = float(model(padded, training=False)[0][0])  # Not model.predict()
        
        return {
            'sentiment': "Positive" if prediction > 0.4 else "Negative",  # Adjusted threshold
            'confidence': max(prediction, 1 - prediction),
            'raw_score': prediction
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")
        raise