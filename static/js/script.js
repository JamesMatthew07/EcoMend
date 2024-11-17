const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const captureButton = document.getElementById('capture');
        const prediction = document.getElementById('prediction');

        // Get access to the camera
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                video.srcObject = stream;
            })
            .catch((err) => {
                console.error("Error accessing the camera: " + err);
            });

        // Capture the image from the video stream
        captureButton.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Convert the image to a base64 string
            const imageData = canvas.toDataURL('image/png');

            // Send the image data to the server
            fetch('/predict', {
                method: 'POST',
                body: JSON.stringify({ image: imageData }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    prediction.textContent = `Error: ${data.error}`;
                } else {
                    prediction.textContent = `Veg/Fruit in image is: ${data.predicted_class} with confidence: ${data.confidence}`;
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                prediction.textContent = 'Error processing the image';
            });
        });