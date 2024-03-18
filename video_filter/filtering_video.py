import cv2
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions


def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    # Extract frames from the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()

    # Analyze each frame using a pre-trained ResNet50 model
    for frame in frames:
        if is_explicit_frame(frame):
            return True  # Explicit content detected in at least one frame

    return False  # No explicit content detected


def is_explicit_frame(frame):
    # Load a pre-trained ResNet50 model for image classification
    model = ResNet50(weights='imagenet')

    # Resize the frame to the model's expected input size
    resized_frame = cv2.resize(frame, (224, 224))
    resized_frame = np.expand_dims(resized_frame, axis=0)

    # Preprocess the frame
    preprocessed_frame = preprocess_input(resized_frame)

    # Make predictions using the model
    predictions = model.predict(preprocessed_frame)

    # Decode the predictions
    decoded_predictions = decode_predictions(predictions)

    # Check if any prediction indicates explicit content
    for _, label, confidence in decoded_predictions[0]:
        if 'porn' in label.lower() and confidence > 0.5:
            return True  # Explicit content detected

    return False  # No explicit content detected


# Example usage
video_path = 'path/to/your/video.mp4'
is_explicit = analyze_video(video_path)

if is_explicit:
    print("Explicit content detected in the video.")
else:
    print("No explicit content detected in the video.")
