import tensorflow as tf
import streamlit as st
import numpy as np
from tensorflow import keras

st.header('Real-Time Image Classification with Camera')

# Load the model using keras.models.load_model()
try:
    model = keras.models.load_model('C:/Users/James/OneDrive/Desktop/EcoMend/Image_classify.keras')
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

data_cat = ['plastic', 'paper']

img_height = 180
img_width = 180

# Use Streamlit's camera input to capture an image
image = st.camera_input("Capture an image with your camera")

if image is not None:
    try:
        # Load and preprocess the image
        image_load = tf.image.decode_image(image.read(), channels=3)
        image_load = tf.image.resize(image_load, [img_height, img_width])
        img_bat = tf.expand_dims(image_load, 0)  # Add batch dimension

        # Use the loaded model for prediction
        predictions = model.predict(img_bat)
        score = tf.nn.softmax(predictions[0])

        predicted_class = data_cat[np.argmax(score)]
        confidence = np.max(score) * 100

        # Display results
        st.image(image, width=200)
        st.write(f'Veg/Fruit in image is: **{predicted_class}**')
        st.write(f'With accuracy of: **{confidence:.2f}%**')

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
