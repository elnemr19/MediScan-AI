from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO

# Load pneumonia model
pneumonia_model = load_model('models/simpleCNN_pneumonia.h5')

# Load brain tumor model
brain_model = load_model('models/brain_tumor_model.h5')


# Function to predict pneumonia
def predict_pneumonia(img):
    # Convert the FileStorage object to a BytesIO stream
    img_stream = BytesIO(img.read())
    
    # Load the image from the stream
    img = image.load_img(img_stream, target_size=(224, 224))
    
    # Convert the image to a numpy array and normalize it
    img_array = image.img_to_array(img) / 255.0
    
    # Add an extra dimension to match the input shape of the model
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict using the loaded model
    prediction = pneumonia_model.predict(img_array)
    
    # Return prediction result
    return "Pneumonia" if prediction > 0.5 else "No Pneumonia"


# Function to predict brain tumor
class_names = ['brain_meningioma', 'brain_tumor', 'brain_glioma']

# Function to predict brain tumor
def predict_brain_tumor(img):
    # Convert the FileStorage object to a BytesIO stream
    img_stream = BytesIO(img.read())  # Read file content as bytes and convert it to a stream
    
    # Load the image from the stream
    img = image.load_img(img_stream, target_size=(224, 224))  # Ensure it's the right size
    
    # Convert the image to a numpy array and normalize it
    img_array = image.img_to_array(img) / 255.0  # Normalize the image
    
    # Add an extra dimension to match the model's input shape (batch_size, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict using the brain tumor model (multi-class)
    prediction = brain_model.predict(img_array)
    
    # Get the class with the highest probability
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    
    # Map the predicted class index to the class name
    predicted_class = class_names[predicted_class_index]
    
    return predicted_class