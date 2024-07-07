from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
import tensorflow as tf
from collections import deque

app = Flask(__name__)

# Load your pretrained model
model = tf.keras.models.load_model('LRCN_model__Date_Time_2024_07_07__16_03_46__Loss_0.39749324321746826__Accuracy_0.8640000224113464.h5')

# Constants
IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
SEQUENCE_LENGTH = 20
CLASSES_LIST = ["WalkingWithDog", "TaiChi", "JumpRope", "HorseRace"]

def frames_extraction(video_path):
    frames_list = []
    video_reader = cv2.VideoCapture(video_path)
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH), 1)

    for frame_counter in range(SEQUENCE_LENGTH):
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)
        success, frame = video_reader.read()
        if not success:
            break
        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        normalized_frame = resized_frame / 255
        frames_list.append(normalized_frame)

    video_reader.release()
    return frames_list

def predict_on_video(video_file_path, output_file_path, SEQUENCE_LENGTH):
    video_reader = cv2.VideoCapture(video_file_path)
    Original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    Original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'),
                                   video_reader.get(cv2.CAP_PROP_FPS), (Original_video_width, Original_video_height))
    
    frames_queue = deque(maxlen=SEQUENCE_LENGTH)
    predicted_class_name = ''

    while video_reader.isOpened():
        ok, frame = video_reader.read()
        if not ok:
            break
        
        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        normalized_frame = resized_frame / 255
        frames_queue.append(normalized_frame)

        if len(frames_queue) == SEQUENCE_LENGTH:
            predicted_labels_probabilities = model.predict(np.expand_dims(frames_queue, axis = 0))[0]
            predicted_label = np.argmax(predicted_labels_probabilities)
            predicted_class_name = CLASSES_LIST[predicted_label]

        cv2.putText(frame, predicted_class_name, (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 5)
        video_writer.write(frame)
    
    video_reader.release()
    video_writer.release()

@app.route('/predict', methods=['POST'])
def predict():
    if 'video' not in request.files:
        return "Please provide a video file", 400
    
    video_file = request.files['video']
    input_video_path = 'input_video.mp4'
    output_video_path = 'output_video.mp4'
    video_file.save(input_video_path)
    
    predict_on_video(input_video_path, output_video_path, SEQUENCE_LENGTH)
    
    return send_file(output_video_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5000/predict