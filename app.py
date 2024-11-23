import tensorflow as tf
import streamlit as st
import numpy as np
from tensorflow import keras
import time  # For controlling the refresh rate

# App header
st.title('Real-Time Object Detection with Continuous Scanning')

# Load the trained model
try:
    model = keras.models.load_model('C:/Users/James/OneDrive/Desktop/EcoMend/Image_classify.keras')
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

# Define categories
data_cat = ['disposable cup', 'paper', 'plastic bottle']

# Set image dimensions
img_height = 224
img_width = 224

# Display a message
st.info("Place an object in front of the camera for continuous scanning.")

# Camera input
image = st.camera_input("Real-Time Camera", key="camera_input")

if image is not None:
    # Run continuous scanning
    while True:
        try:
            # Preprocess the image for prediction
            image_load = tf.image.decode_image(image.read(), channels=3)
            image_load = tf.image.resize(image_load, [img_height, img_width])
            img_bat = tf.expand_dims(image_load, 0)  # Add batch dimension

            # Perform prediction
            predictions = model.predict(img_bat)
            score = tf.nn.softmax(predictions[0])

            # Determine the predicted class and confidence
            predicted_class = data_cat[np.argmax(score)]
            confidence = np.max(score) * 100

            # Display the results
            st.image(image, caption="Captured Image", width=300)
            st.write(f"### Prediction: **{predicted_class}**")
            st.write(f"### Confidence: **{confidence:.2f}%**")

            # Refresh rate for scanning (e.g., every 1 second)
            time.sleep(1)

        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")
            break
