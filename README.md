# Action Recognition
Welcome to the **Action Recognition** repository!. This project leverages cutting-edge computer vision and machine learning technologies to detect action in a video.

## 📄 Introduction
This project aims to develop a comprehensive system for motion detection and object detection in ICU videos. The primary objectives are:
- This Flask application uses a pretrained TensorFlow model to classify activities in video files, predicting classes like "WalkingWithDog" and "TaiChi." 
- Processes video frames with OpenCV, resizing and normalizing them before making predictions.


## 🗂 Table of Contents
- [Introduction](#-introduction)
- [Requirements](#-requirements)
- [Output Video](#-output-video)
- [Preprocessing](#-preprocessing)
- [Features](#-features)
- [API Integration](#-api-integration)
- [Output](#-output)
- [Conclusion](#-conclusion)
- [Get Started](#-get-started)

## 📦 Requirements
1. [PyGame](https://www.pygame.org/docs/)
2. [OpenCV Python Library](https://docs.opencv.org/4.x/)
3. [Numpy Python Library](https://numpy.org/doc/)
4. [Tensorflow Python Library](https://www.tensorflow.org/api_docs)
5. [PyDot Python Library](https://pypi.org/project/pydot/)
6. [Matplotlib Python Library](https://matplotlib.org/stable/index.html)
7. [MoviePy Python Library](https://pypi.org/project/moviepy/)
8. [Scikit-Learn Python Library](https://scikit-learn.org/0.21/documentation.html)
9. [Youtube_Dl Python Library](https://youtube-dl.readthedocs.io/en/latest/)
10. [Postman Software](https://learning.postman.com/docs/introduction/overview/)

## 🎥 Output Video
https://github.com/AmanStarLitePro/Action-Recognition/assets/143260479/f607f36b-bc25-45bc-9a63-7ef70e37155d

## 🛠 Preprocessing
![Preprocessing](https://github.com/AmanStarLitePro/Action-Recognition/assets/143260479/2862174d-c9e0-4506-9d83-9798d2f92b4b)

## 🎯 Features

**API Functionalities**
- **Predict**: Accessible using POSTMAN software with a JSON request, returning output video of action detection.

**Server Access**
- API accessible via the local host server at `http://127.0.0.1:5000`.

## 📬 API Integration
To access the API using Postman, follow these steps:

- Install Postman:

- If you haven't already, download and install Postman from [here](https://www.postman.com/downloads/).

- Open Postman: Start the Postman application.

- Create a New Request: Click on the "New" button and select "HTTP Request".

- Set Request Type: Change the request type to POST.

- Enter the URL: In the request URL field, enter the endpoint URL: http://127.0.0.1:5000/predict.

- Add Video File:

- Click on the "Body" tab below the URL field.
   - Select "form-data".
   - In the "Key" field, enter video.
   - In the "Value" field, click on the dropdown and select "File".
   - Choose the video file you want to upload.

- Send the Request: Click the "Send" button.

- Receive the Response:
  - If the request is successful, the response should contain the annotated video file.
  - You can download and view this video to see the predictions overlaid on the frames.

For more details on using Postman, refer to the [Postman Documentation](https://learning.postman.com/docs/introduction/overview/).

## 📊 Output
![Accuracy Vs Validation](https://github.com/AmanStarLitePro/Action-Recognition/assets/143260479/aba1eaec-3574-4cc1-91eb-325d93bcfd47)

## 🏁 Conclusion
This project is a video classification service that uses a LRCN (Long-term Recurrent Convolutional Network) model to predict activities in a video. It loads the model, extracts and preprocesses frames from an input video, and uses the model to predict the activity class for these frames. The predictions are overlaid on the video frames, and the annotated video is saved. The Flask app exposes a `/predict` endpoint, which accepts a video file via a POST request, processes the video to make predictions, and returns the annotated video. This enables seamless integration of video classification capabilities into other systems or applications.

Future work will focus on improving the models’ accuracy, expanding the dataset, and exploring additional functionalities to enhance the system’s capabilities.

## 🚀 Get Started

**Install Dependencies and Run the API:**

```sh
pip install -r requirements.txt
python api.py

Thank you for checking out our project! If you have any questions or feedback, feel free to reach out to us.

