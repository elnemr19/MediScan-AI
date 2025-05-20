import tensorflow as tf
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sys
import os

# Disable oneDNN optimizations for consistency
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def predict(text):
    try:
        # 1. Load model and tokenizer
        model = tf.keras.models.load_model("models/sentiment_analysis_model.keras", compile=False)
        with open("models/tokenizer.pkl", "rb") as f:
            tokenizer = pickle.load(f)
        
        # 2. Preprocess input
        seq = tokenizer.texts_to_sequences([text])
        if not seq or not seq[0]:
            return 0.5  # Neutral score if no tokens found
            
        padded = pad_sequences(seq, maxlen=300, padding="post")
        
        # 3. Predict
        return float(model.predict(padded, verbose=0)[0][0])
        
    except Exception as e:
        print(f"Prediction error: {str(e)}", file=sys.stderr)
        return 0.5  # Fallback neutral score

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python isolated_predictor.py \"Your text here\"")
        print("Testing with default text...")
        test_text = "this system is very good"
        print(f"Text: '{test_text}'")
        score = predict(test_text)
        print(f"Result: {score:.4f}")
    else:
        text = sys.argv[1]
        print(predict(text))