# 🧠 MediScan-AI: AI-Powered Medical Diagnostic Platform

MediScan-AI is an integrated AI system designed to assist medical professionals and patients with fast, accurate diagnostic tools powered by deep learning. This web-based platform includes medical image classification, drug identification, patient feedback analysis, and an AI-driven chatbot — all accessible through a user-friendly interface.

![image](https://github.com/user-attachments/assets/7ab71fd3-e0a3-44a8-b821-a3577ba6253e)


---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
  - [Pneumonia Detection](#1-pneumonia-detection)
  - [Brain Tumor Detection](#2-brain-tumor-detection)
  - [Drug Classification](#3-drug-classification)
  - [Sentiment Analysis](#4-sentiment-analysis)
  - [Medical Chatbot](#5-medical-chatbot)
  - [User Authentication](#6-user-authentication)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation & Usage](#installation--usage)
- [Team](#team)
- [License](#license)

---

## 🧭 Overview

**MediScan-AI** aims to provide a fast, intelligent, and scalable tool that supports early detection and classification of medical conditions, assists in drug recognition, and enhances patient experience with sentiment analysis and intelligent Q&A. The platform combines multiple AI models into a unified Flask-based application.

---

## 🔍 Features

### 1. 🫁 Pneumonia Detection

#### 🧠 What is it?
Pneumonia is a severe lung infection that can be life-threatening if not diagnosed early. Detecting it through chest X-rays is a common diagnostic practice.

#### 🏥 What does this feature do?
- Allows the user to **upload a chest X-ray image**.
- The AI model analyzes the image and classifies it as either:
  - **Normal**
  - **Pneumonia**

#### 🧪 Dataset Used:
- **Kaggle Chest X-ray Dataset**
  - Contains labeled X-ray images categorized into "NORMAL" and "PNEUMONIA".
  - [Link to dataset](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia)

#### 🤖 Model Details:
- **Convolutional Neural Network (CNN)**
- **DenseNet121** (transfer learning model)
- Trained with augmented images to improve generalization.
- You can check the code from [Her](https://www.kaggle.com/code/abdullahalnemr/chest-x-ray-images-densenet)

#### ⚙️ Workflow:
1. User uploads a chest X-ray.
2. Image is preprocessed and resized.
3. The model predicts the label.
4. Result is displayed in the UI.

---

### 2. 🧠 Brain Tumor Detection

#### 🧠 What is it?
Brain tumors are abnormal growths in brain tissues. Early identification of tumor type is critical for treatment planning.

#### 🏥 What does this feature do?
- Accepts a **brain MRI image** upload.
- Classifies into one of three categories:
  - **Glioma Tumor**
  - **Meningioma Tumor**
  - **No Tumor**

#### 🧪 Dataset Used:
- Publicly available brain tumor MRI dataset
- Contains categorized MRI scans labeled with tumor types.

#### 🤖 Model Details:
- **CNN + EfficientNet-B0**
- EfficientNet is a state-of-the-art lightweight image classification architecture.
- Fine-tuned for high performance on medical images.

#### ⚙️ Workflow:
1. User uploads an MRI image.
2. Preprocessing and normalization applied.
3. Model returns the tumor category.
4. Diagnosis is presented clearly.

---

### 3. 💊 Drug Classification

#### 🧠 What is it?
Identifying pharmaceutical drugs by image can assist pharmacists, patients, and healthcare systems, especially in low-resource environments.

#### 🏥 What does this feature do?
- Upload an image of a **pharmaceutical drug**.
- The system classifies it into one of **10 predefined drug categories**.
  - Example categories: *Alaxan, Bioflu, Fish Oil, Decolgen*, etc.

#### 🧪 Dataset Used:
- Custom drug image dataset collected and organized into 10 categories.
- Dataset augmented using rotation, zoom, and flip techniques.
- [Pharmaceutical Drugs and Vitamins Synthetic Images](https://www.kaggle.com/datasets/vencerlanz09/pharmaceutical-drugs-and-vitamins-synthetic-images)

#### 🤖 Model Details:
- **Custom-built CNN model**
- Trained from scratch using image augmentation for robustness.
- - You can check the code from [Her](https://www.kaggle.com/code/abdullahalnemr/pharmaceutical-drugs-97)

#### ⚙️ Workflow:
1. User uploads a drug image.
2. Image is processed.
3. Model predicts the class label.
4. Drug name is displayed as output.

---

### 4. 💬 Sentiment Analysis

#### 🧠 What is it?
Understanding user feedback is essential for improving healthcare platforms. Sentiment analysis classifies reviews as **positive** or **negative**.

#### 🏥 What does this feature do?
- Users submit a **text review** about the system.
- The model analyzes and returns the **sentiment**.

#### 🧪 Dataset Used:
- Text dataset with labeled positive and negative reviews.

#### 🤖 Model Details:
- **LSTM (Long Short-Term Memory) neural network**
- Designed to understand sequential word patterns and emotions.
- You can check the code from [Her](https://www.kaggle.com/code/abdullahalnemr/twitter-sentiment-analysis-lstm-98)

#### ⚙️ Workflow:
1. User submits a review.
2. Text is tokenized and padded.
3. LSTM processes and predicts sentiment.
4. Feedback is displayed as positive/negative.

---

### 5. 🤖 Medical Chatbot

#### 🧠 What is it?
Medical chatbots assist users by answering health-related questions instantly using large language models.

#### 🏥 What does this feature do?
- User types a **medical question**.
- The chatbot provides an **intelligent and medically-relevant response**.

#### 🧠 Model Used:
- **Qwen 1.8B** (Large Language Model)
- Accessed through the **Olama API** (hosted LLM inference)

#### ⚙️ Workflow:
1. User submits a question.
2. API sends it to Qwen 1.8B model.
3. Response is displayed in the chat interface.

---

### 6. 🔐 User Authentication

#### 🔐 What does this feature do?
- Provides **login functionality** to secure the platform.
- Ensures authorized access using Flask session-based authentication.

---

## 🧠 Technologies Used

| Technology        | Purpose                                |
|------------------|----------------------------------------|
| Python           | Core language                          |
| Flask            | Web application framework              |
| TensorFlow       | Deep learning backend                  |
| PyTorch          | Used for specific models (e.g., LSTM)  |
| OpenCV           | Image preprocessing                    |
| HTML/CSS/JavaScript | Frontend styling & interactivity     |
| Qwen 1.8B + Olama API | Medical chatbot responses        |
| Jinja2           | Templating engine                      |

---

## 🏗 Project Structure

mediscan-ai/

├── app.py # Flask entry point

├── config.py # Config settings

├── auth.py # Auth logic

├── models/ # Trained .h5 models

├── views/ # Blueprints for each module

├── templates/ # Jinja2 HTML files

├── static/ # CSS, JS, Images

├── utils/ # Helper utilities

├── requirements.txt # Dependencies

└── README.md




## 🎬 Demo Video




