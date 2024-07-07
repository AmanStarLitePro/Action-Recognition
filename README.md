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
1. [Ultralytics Python Library](https://docs.ultralytics.com/)
2. [OpenCV Python Library](https://docs.opencv.org/4.x/)
3. [Numpy Python Library](https://numpy.org/doc/)
4. [Tensorflow Python Library](https://www.tensorflow.org/api_docs)
5. [Pyyaml Python Library](https://pyyaml.org/wiki/PyYAMLDocumentation)
6. [Postman Software](https://learning.postman.com/docs/introduction/overview/)

## 🎥 Output Video
https://github.com/AmanStarLitePro/Action-Recognition/assets/143260479/f607f36b-bc25-45bc-9a63-7ef70e37155d

## 🛠 Preprocessing
![Preprocessing](https://github.com/AmanStarLitePro/Action-Recognition/assets/143260479/2862174d-c9e0-4506-9d83-9798d2f92b4b)

## 🎯 Features

**API Functionalities**
- **Predict**: Accessible using POSTMAN software with a JSON request, returning output video of action detection.

**Server Access**
- API accessible via the local host server at `http://127.0.0.1:5000`.

 ## 📬 Access API Using Postman Software Using JSON
To access the API using Postman, follow these steps:

Install Postman:

If you haven't already, download and install Postman from [here](https://www.postman.com/downloads/).
Create a New Request:

Open Postman and click on New to create a new HTTP request.
Set the Request Type and URL:

Select POST as the request type.
Enter the API endpoint URL: http://127.0.0.1:5000/predict.
Set Headers:

Click on the Headers tab and add the following key-value pair:
Content-Type: application/json
Set the Body:

Click on the Body tab and select raw and JSON (application/json).
Enter the JSON payload with the video data you want to process. For example:

Copy code
{
  "video_path": "path/to/your/video.mp4"
}

Send the Request:
Click on Send to submit your request to the API.
You should receive a response with the processed frames and video output.

For more details on using Postman, refer to the [Postman Documentation](https://learning.postman.com/docs/introduction/overview/).

## 📊 Output
![Accuracy Vs Validation](https://github.com/AmanStarLitePro/Action-Recognition/assets/143260479/aba1eaec-3574-4cc1-91eb-325d93bcfd47)

## 🏁 Conclusion
This project outlines the steps taken to develop and integrate a motion detection and object detection system for ICU videos. The combination of YOLOv8s and LSTM models has provided a robust solution for the project's objectives. The API integration further enhances usability, making it easier to deploy and utilize the system in real-world scenarios.

Future work will focus on improving the models’ accuracy, expanding the dataset, and exploring additional functionalities to enhance the system’s capabilities.

## 🚀 Get Started

**Install Dependencies and Run the API:**

```sh
pip install -r requirements.txt
python main.py

## Access the API:
Open your browser and go to http://127.0.0.1:9000/index.


Thank you for checking out our project! If you have any questions or feedback, feel free to reach out to us.

