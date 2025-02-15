import os
import cv2
import pafy
# import pydot
# import pygame
# pip install youtube_dl
import math
import random
import numpy as np
import datetime as dt
import tensorflow as tf
from collections import deque
import matplotlib.pyplot as plt
from moviepy.editor import *
from sklearn.model_selection import train_test_split

# from tensorflow.keras.layers import *
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.callbacks import EarlyStopping
# from tensorflow.keras.utils import plot_model


# Set Numpy , Python and Tensorflow seeds to get consistent result on every execution
seed_constant = 27
np.random.seed(seed_constant)
random.seed(seed_constant)
tf.random.set_seed(seed_constant)

# Download Dataset
# https://www.crcv.ucf.edu/data/UCF50.rar

# For visualisation, we will pick 20 random categories from the dataset and a random
# video from each selected category and will visualize the first frame of the
# the selected videos with their associated labels written. This way we'll 
# visualize a subset (20 random videos) of the dataset.

# Create a matplotlib figure and specify the size of the figure
plt.figure(figsize= (20,20))

# Get the names of all classes/categories in UCF50
all_classes_names = os.listdir('UCF50')
# print(all_classes_names)

# Generate the list of 20 random values. The Values will be between 0-50,
# Where 50 is the total classes in the dataset
random_range = random.sample(range(len(all_classes_names)), 20)

plt.figure(figsize=(20,20))

# Iterating through all the generated random values.
for counter, random_index in enumerate(random_range, 1):

    # Retreive a Class Name using the random index.
    selected_class_Name = all_classes_names[random_index]

    # Retreive the list of all the video files present in the randomly selected Class Directory.
    video_files_names_list = os.listdir(f'UCF50/{selected_class_Name}')

    # Randomly select a video file from the list retreived from the
    # randomly selected Class Directory
    selected_video_file_name = random.choice(video_files_names_list)

    # Initialize a VideoCapture object to read from the video file.
    video_reader = cv2.VideoCapture(f'UCF50/{selected_class_Name}/{selected_video_file_name}')

    # Read the first frame of the Video File
    _, bgr_frame = video_reader.read()

    # Release the videoCapture Object.
    video_reader.release()

    # Convert the frame from BGR into RGB format.
    rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)

    # Write the class name on the video frame
    cv2.putText(rgb_frame, selected_class_Name, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(rgb_frame, "DETECTED", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    
    # Display the frame
    plt.subplot(5, 4, counter) 
    plt.imshow(rgb_frame)
    plt.axis('off')
# plt.show()

# ---------------------------------------------------------------------

#                          Preprocessing the data

# Specify the height and width to which each video frame will be resized in our dataset.
IMAGE_HEIGHT , IMAGE_WIDTH = 64, 64

# Specify the number of frames of a video that will be fed to the model as one sequence.
SEQUENCE_LENGTH = 20

# Specify the directory containing the UCF50 dataset.
DATASET_DIR = 'UCF50'

# Specify the list containing the names of the classes used for training.
# We can also choose any set of classes here
CLASSES_LIST = ["WalkingWithDog", "TaiChi", "JumpRope", "HorseRace"]


# Creating a Function to Extract, Resize and Normalize Frames
def frames_extraction(video_path):
    # This function will extract the requried frames from a video after resizing
    # and Normalizing them.
    # Arguments : 
    #   video_path : The path of the video in the disk, whose frames are to be extracted.
    # Returns :
    # frames_list: A list containing the resized and normalized frames of the video.

    # Declare a list to store video frames.
    frames_list = []

    # Read the Video File using the VideoCapture object.
    video_reader = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video.
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval after which frames will be added to the list.
    skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH), 1)

    # Iterate through the Video Frames.
    for frame_counter in range(SEQUENCE_LENGTH):

        # Set the current frame position of the video.
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

        # Reading the frame from the video.
        success, frame = video_reader.read()

        # Check if Video frame is not successfully read then break the loop
        if not success:
            break

        # Resize the Frame to fixed height and width.
        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))

        # Normalize the resized frame by dividing it with 255 so that each pixel 
        # value then lies between 0 and 1
        normalized_frame = resized_frame / 255

        # Append the normalized frame into the frames list
        frames_list.append(normalized_frame)

    # Release the VideoCapture Object.
    video_reader.release()

    # Return the frames list.
    return frames_list

#  Creating a function for Dataset Creation
def create_dataset():
    # This function will extract the data of the selected classes and create
    # the required dataset.
    # Returns:
    #   Features: A list containing the extracted frames of the videos.
    #   Labels: A list containing the indexes of the classes associated with the videos.
    #   video_files_paths: A list containing the paths of the videos in the disk.

    # Declaring Empty Lists to store the features, labels and video file path values.
    features = []
    labels = []
    video_files_paths = []

    # Iterating through all the classes mentioned in the classes list.
    for class_index, class_name, in enumerate(CLASSES_LIST):

        # Display the name of the class whose data is being extracted.
        print(f'Extracting Data of Class: {class_name}')

        # Get the list of video files present in the specific class name directory.
        files_list = os.listdir(os.path.join(DATASET_DIR, class_name))

        # Iterate through all the files present in the files list.
        for file_name in files_list:

            # Get the complete video path.
            video_file_path = os.path.join(DATASET_DIR, class_name, file_name)

            # Extract the frames of the video file
            frames = frames_extraction(video_file_path)

            # Check if the extracted frames are equal to the SEQUENCE_LENGTH specified above
            # So ignore the video having frames less than the SEQUENCE_LENGTH.
            if len(frames) == SEQUENCE_LENGTH:

                # Append the data to their respective lists.
                features.append(frames)
                labels.append(class_index)
                video_files_paths.append(video_file_path)

    # Converting the list to numpy arrays
    features = np.asarray(features)
    labels = np.array(labels)

    # Return the frames, class index, and video file path.
    return features, labels, video_files_paths


# Now we will utilize the function create dataset() created above to 
# extract the data of the selected classes and create the required dataset.

# Create the dataset.
features, labels, video_files_paths = create_dataset()

# Now we will convert labels(class indexes) into one-hot encoded vectors.
# Using Keras's to_categorical method to convert labels into one-hot encoded vectors.
one_hot_encoded_labels = tf.keras.utils.to_categorical(labels)


#                       Splitting the Data into Train and Test Set

# Split the Data into Train(75%) and Test Set(25%)
features_train, features_test, labels_train, labels_test = train_test_split(
    features, one_hot_encoded_labels, test_size=0.25, shuffle=True, 
    random_state = seed_constant
)

#                           # Constructing the model
 
# def create_convlstm_model():
#     # This function will construct the required convlstm model.
#     # returns:
#     #   model: It is the required constructed convlstm model.

#     # We will use a Sequential Model for model construction
#     model = tf.keras.models.Sequential()

#     # Define the Model Architecture.
#     # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

#     model.add(
#         tf.keras.layers.ConvLSTM2D(filters = 4, kernel_size = (3,3),
#                                    activation='tanh', data_format="channels_last",
#                                    recurrent_dropout=0.2, return_sequences=True,
#                                    input_shape = (SEQUENCE_LENGTH, IMAGE_HEIGHT, IMAGE_WIDTH, 3)))
    
#     model.add(tf.keras.layers.MaxPooling3D(pool_size=(1,2,2), padding='same',
#                                            data_format='channels_last'))
    
#     model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(0.2)))
#     model.add(tf.keras.layers.ConvLSTM2D(filters = 8, kernel_size=(3,3), activation='tanh', 
#                          data_format = 'channels_last', recurrent_dropout=0.2,
#                          return_sequences=True))
    
#     model.add(tf.keras.layers.MaxPooling3D(pool_size=(1,2,2), padding='same',
#                                            data_format='channels_last'))
    
#     model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(0.2)))
#     model.add(tf.keras.layers.ConvLSTM2D(filters = 14, kernel_size=(3,3), activation='tanh', 
#                          data_format = 'channels_last', recurrent_dropout=0.2,
#                          return_sequences=True))
    
#     model.add(tf.keras.layers.MaxPooling3D(pool_size=(1,2,2), padding='same',
#                                            data_format='channels_last'))
    
#     model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(0.2)))
#     model.add(tf.keras.layers.ConvLSTM2D(filters = 16, kernel_size=(3,3), activation='tanh', 
#                          data_format = 'channels_last', recurrent_dropout=0.2,
#                          return_sequences=True))
    
#     model.add(tf.keras.layers.MaxPooling3D(pool_size=(1,2,2), padding='same',
#                                            data_format='channels_last'))
#     #model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(0.2)))

#     model.add(tf.keras.layers.Flatten())
#     model.add(tf.keras.layers.Dense(len(CLASSES_LIST), activation="softmax"))

#     # Display the model Summary.
#     model.summary()

#     # Return the constructed model convlstm model
#     return model

# # Now we will utilize the function create_convlstm_model() to construct the
# # required convlstm model.

# # Construct the required convlstm model.
# convlstm_model = create_convlstm_model()

# # Display the success message.
# print("Model Created Successfully!")

# #                       Compile and Train the model

# # Next we will add an early stopping callback to prevent overfitting
# # and start the training after compiling the model.

# # Create an Instance of Early Stopping callback
# early_stopping_callback = tf.keras.callbacks.EarlyStopping(monitor = 'val_loss', patience=10, mode='min', restore_best_weights=True)

# # Compile the model and specify loss function, optimizer and metrices values to the model
# convlstm_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])

# # Start training the model
# convlstm_model_training_history = convlstm_model.fit(x=features_train, y=labels_train, epochs=50, batch_size=4, 
#                                                      shuffle=True, validation_split=0.2,
#                                                      callbacks=[early_stopping_callback])

# #                            Evaluating the model

# # Evaluate the trained model
# model_evaluation_history = convlstm_model.evaluate(features_test, labels_test)


# #                               Save the model 

# # Get the loss and accuracy from model_evaluation_history.
# model_evaluation_loss, model_evaluation_accuracy = model_evaluation_history

# # Define the string date format.
# # Get the current Date and Time in a DateTime Object.
# # Convert the DateTime object to string according to the style mentioned in date_time_format string.
# date_time_format = '%Y_%m_%d__%H_%M_%S'
# current_date_time_dt = dt.datetime.now()
# current_date_time_string = dt.datetime.strftime(current_date_time_dt, date_time_format)

# # Define a useful name for our model to make it easy for us while navigating 
# # through multiple saved models.
# model_file_name = f'convlstm_model__Date_Time_{current_date_time_string}__Loss_{model_evaluation_loss}__Accuracy_{model_evaluation_accuracy}.h5'

# # Save your Model.
# convlstm_model.save(model_file_name)


# #                       Plot Model's Loss And Accuracy Curves

# def plot_metric(model_training_history, metric_name_1, metric_name_2, plot_name):
#     # This function will plot the metrics passed to it in a graph.
#     # Args:
#     #       model_training_history: A history object containing a record of training and validation
#     #                               loss values and metrics values at successive epochs
#     #       metric_name_1: The name of the first metric that needs to be plotted in the graph
#     #       metric_name_2: The name of the second metric that needs to be plotted in the graph
#     #       plot_name: the title of the graph

#     # Get metric values using metric names as identifiers.
#     metric_value_1 = model_training_history.history[metric_name_1]
#     metric_value_2 = model_training_history.history[metric_name_2]

#     # Construct a range object which will be used as x-axis(horizontal plane) of the graph.
#     epochs = range(len(metric_value_1))

#     # Plot the Graph.
#     plt.plot(epochs, metric_value_1, 'blue', label=metric_name_1)
#     plt.plot(epochs, metric_value_2, 'red', label=metric_name_2)

#     # Add the title to the plot
#     plt.title(str(plot_name))

#     # Add legend to the plot
#     plt.legend()
#     plt.show()

# #Now utililze the function plot_metric()

# # Visualize the training and validation loss metrics.
# plot_metric(convlstm_model_training_history, 'loss', 'val_loss', "Total Loss vs Total Validation Loss")

# # Visualize the training and validation accuracy metrics.
# plot_metric(convlstm_model_training_history, 'accuracy', 'val_accuracy', "Total Accuracy vs Total Validation Accuarcy")




# ------------------CONSTRUCTING A NEW MODEL LRCM MODEL-----------------

def create_LRCN_model():
    # This function will construct the required LRCN Model.
    # Returns:
    #   model: It is the required constructed model.

    # We will use a Sequential model for model construction.
    model = tf.keras.models.Sequential()

    # Define the model achitecture
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(16, (3,3), padding='same', activation='relu'),
                              input_shape = (SEQUENCE_LENGTH, IMAGE_HEIGHT, IMAGE_WIDTH, 3)))
    
    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.MaxPooling2D((4,4))))
    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(0.25)))

    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(32, (3,3), padding='same', activation='relu')))
    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.MaxPooling2D((4,4))))
    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(0.25)))

    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu')))
    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.MaxPooling2D((2,2))))
    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(0.25)))

    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu')))
    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.MaxPooling2D((2,2))))
    # model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(0.25)))

    model.add(tf.keras.layers.TimeDistributed(tf.keras.layers.Flatten()))

    model.add(tf.keras.layers.LSTM(32))
    model.add(tf.keras.layers.Dense(len(CLASSES_LIST), activation='softmax'))

    # Display the models summary.
    model.summary()
    
    # Return the constructed LRCN model
    return model

# Now we will utilize the function create_LRCN_model()

# Construct the required LRCN model.
LRCN_model = create_LRCN_model()

# Display the success message
print("Model Created Successfully!")

#                       Compile and Train LRCN Model

# Next we will add an early stopping callback to prevent overfitting
# and start the training after compiling the model.

# Create an Instance of Early Stopping callback
early_stopping_callback = tf.keras.callbacks.EarlyStopping(monitor = 'val_loss', patience=15, mode='min', restore_best_weights=True)

# Compile the model and specify loss function, optimizer and metrices values to the model
LRCN_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])

# Start training the model
LRCN_model_training_history = LRCN_model.fit(x=features_train, y=labels_train, epochs=70, batch_size=4, 
                                                     shuffle=True, validation_split=0.2,
                                                     callbacks=[early_stopping_callback])

#                          Evaluating the LRCN model

# Evaluate the trained model
model_evaluation_history = LRCN_model.evaluate(features_test, labels_test)

#                               Save the LRCN model 

# Get the loss and accuracy from model_evaluation_history.
model_evaluation_loss, model_evaluation_accuracy = model_evaluation_history

# Define the string date format.
# Get the current Date and Time in a DateTime Object.
# Convert the DateTime object to string according to the style mentioned in date_time_format string.
date_time_format = '%Y_%m_%d__%H_%M_%S'
current_date_time_dt = dt.datetime.now()
current_date_time_string = dt.datetime.strftime(current_date_time_dt, date_time_format)

# Define a useful name for our model to make it easy for us while navigating 
# through multiple saved models.
model_file_name = f'LRCN_model__Date_Time_{current_date_time_string}__Loss_{model_evaluation_loss}__Accuracy_{model_evaluation_accuracy}.h5'

# Save your Model.
LRCN_model.save(model_file_name)


#                       Plot Model's Loss And Accuracy Curves

def plot_metric(model_training_history, metric_name_1, metric_name_2, plot_name):
    # This function will plot the metrics passed to it in a graph.
    # Args:
    #       model_training_history: A history object containing a record of training and validation
    #                               loss values and metrics values at successive epochs
    #       metric_name_1: The name of the first metric that needs to be plotted in the graph
    #       metric_name_2: The name of the second metric that needs to be plotted in the graph
    #       plot_name: the title of the graph

    # Get metric values using metric names as identifiers.
    metric_value_1 = model_training_history.history[metric_name_1]
    metric_value_2 = model_training_history.history[metric_name_2]

    # Construct a range object which will be used as x-axis(horizontal plane) of the graph.
    epochs = range(len(metric_value_1))

    # Plot the Graph.
    plt.plot(epochs, metric_value_1, 'blue', label=metric_name_1)
    plt.plot(epochs, metric_value_2, 'red', label=metric_name_2)

    # Add the title to the plot
    plt.title(str(plot_name))

    # Add legend to the plot
    plt.legend()
    plt.show()

# Visualize the training and validation loss metrics.
plot_metric(LRCN_model_training_history, 'loss', 'val_loss', "Total Loss vs Total Validation Loss")

# Visualize the training and validation accuracy metrics.
plot_metric(LRCN_model_training_history, 'accuracy', 'val_accuracy', "Total Accuracy vs Total Validation Accuarcy")

#                       Defininig Download Youtube Videos Function

def download_youtube_videos(youtube_video_url, output_directory):
    # This function downloads the youtube video whose URL is passed to it as an argument.
    # Args:
    #   youtube_video_url: URL of the video that URL is passed to it as an argument.
    #   output_directory: The directory path to which the video needs to be stored after downloading.
    # Returns:
    #   title: The title of the downloaded youtube video

    # Create a video object which contains useful information about the video
    video = pafy.new(youtube_video_url)

    # Retreive the title of the video
    title = video.title

    # Get the best available quality object for the video
    video_best = video.getbest()

    # Construct the output file path
    output_file_path = f'{output_directory}/{title}.mp4'

    # Download the youtube video at the best available quality and store it to the constructed path
    video_best.download(filepath = output_file_path, quiet=True)

    # Return the video title
    return title

# # Now we will utilize the function download_youtube_videos() to download 
# # a youtube video on which the LRCN model will be tested

# Make the output directory if it does not exist
test_videos_directory = 'test_videos'
os.makedirs(test_videos_directory, exist_ok=True)

# ************************************************************************

# # Download a YouTube video.
# video_title = download_youtube_videos('https://www.youtube.com/watch?v=8u0qjmHI0cE', test_videos_directory)

# # Get the Youtube Video's path we just downloaded
# input_video_file_path = f'{test_videos_directory}/{video_title}.mp4'

# #           Create a Function To Perform Action Recognition on Videos

# def predict_on_video(video_file_path, output_file_path, SEQUENCE_LENGTH):

#     # This function will perform action recognition on a video using LRCN model
#     # Args:
#     #    video_file_path: The path of the video stored in the disk on which the action recognition is to be performed
#     #    output_file_path: The path where the output video with the prediction action being performed overlayed will be stored.
#     #    SEQUENCE_LENGTH: The fixed number of frames of a video that can be passed to the model as one sequence.

#     # Initialize the VideoCapture object to read form the video file
#     video_reader = cv2.VideoCapture(video_file_path)

#     # Get the width and height of the video
#     Original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
#     Original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # Initialize the VideoWriter Object to store the output video in the disk
#     video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'),
#                                    video_reader.get(cv2.CAP_PROP_FPS), (Original_video_width, Original_video_height))
    
#     # Declare a queue to store video frames.
#     frames_queue = deque(maxlen=SEQUENCE_LENGTH)

#     # Initialize a variable to store the predicted action being performed in the video.
#     predicted_class_name = ''

#     # Iterate until the video is accessed successfully.
#     while video_reader.isOpened():

#         # Read the frame.
#         ok, frame = video_reader.read()

#         # Check if frame is not read properly then break the loop.
#         if not ok:
#              break
        
#         # Resize the frame to fixed Dimensions.
#         resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))

#         # Normalize the resized frame by dividing it with 255 so that each pixel value then lies between 0 and 1
#         normalized_frame = resized_frame / 255

#         # Appending the preprocessed frame into the frames list.
#         frames_queue.append(normalized_frame)

#         # Check if the number of frames to the model and get the predicted probabilities.
#         if len(frames_queue) == SEQUENCE_LENGTH:

#             # Pass the normalized frames to the model and get the predicted probablities.
#             predicted_label_probabilities = LRCN_model.predict(np.expand_dims(frames_queue, axis=0))[0]

#             # Get the index of class with the highest probability
#             predicted_label = np.argmax(predicted_label_probabilities)

#             # Get the class name using the retreived index
#             predicted_class_name = CLASSES_LIST[predicted_label]

#         # Write predicted class name on top of the frame
#         cv2.putText(frame, predicted_class_name, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         # Write the frame into the disk using the VideoWriter Object
#         video_writer.write(frame)

#     # Release the VideoCapture and VideoWriter Objects
#     video_reader.release()
#     video_writer.release()


# #                Perform Action Recognition on Test Video

# # Construct the output video path
# output_video_file_path = f'{test_videos_directory}/{video_title}--Output-SeqLen{SEQUENCE_LENGTH}.mp4'

# # Perform Action Recognition on the Test Video
# predict_on_video(input_video_file_path, output_video_file_path, SEQUENCE_LENGTH)

# # Display the output video
# VideoFileClip(output_video_file_path, audio=False, target_resolution=(300, None)).ipython_display()

# *********************************************************************

#           Create a Function To perform a Single Prediction on Videos

def predict_single_action(video_file_path, SEQUENCE_LENGTH):
    # This function will perform single action recognition on a video using the LRCN model.
    # Args:
    #   video_file_path: The path of the video stored in the disk on which the action recognition is to be performed
    #   SEQUENCE_LENGTH: The fixed number of frames of a video that can be passed to the model as one sequence.

    # Initialize the VideoCapture object to read from the video file.
    video_reader = cv2.VideoCapture(video_file_path)

    # Get the width and height of the video.
    original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Declares a list to store video frames we will extract.
    frames_list = []

    # Initialize a variable to store the predicted action being performed in the video.
    predcicted_class_name = ''

    # Get the number of frames in the video
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval after which frames will be added to the list.
    skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH),1)

    # Iterating the number of times equal to the fixed length of the sequence
    for frame_counter in range(SEQUENCE_LENGTH):

        # Set the current frame position of the video
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

        # Read a frame
        success, frame = video_reader.read()

        # Check if frame is not read properly then break the loop
        if not success:
            break

        # Resized the Frame to fixed Dimensions
        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))

        # Normalize the resized frame by dividing it with 255 so that each pixel value then lies between 0 and 1
        normalized_frame = resized_frame / 255

        # Appending the preprocessed frame into the frames list.
        frames_list.append(normalized_frame)

    # Pass the normalized frames to the model and get the predicted probablities.
    predicted_label_probabilities = LRCN_model.predict(np.expand_dims(frames_list, axis=0))[0]

    # Get the index of class with the highest probability
    predicted_label = np.argmax(predicted_label_probabilities)

    # Get the class name using the retreived index
    predicted_class_name = CLASSES_LIST[predicted_label]

    # Display the predicted action along with the prediction confidence.
    print(f'Action Predicted : {predicted_class_name}\nConfidence : {predicted_label_probabilities[predicted_label]}')

    # Release the VideoCapture and VideoWriter Objects
    video_reader.release()


#               Perform Single prediction on a Test Video

# Download the youtube video
# video_title = download_youtube_videos('https://youtu.be/fc3w827kwyA', test_videos_directory)

# Construct the input youtube video path
input_video_file_path = 'test.mp4'

# Perform Single Prediction on the Test Video
predict_single_action(input_video_file_path, SEQUENCE_LENGTH)

# Display the input Video
clip = VideoFileClip(input_video_file_path, audio=False, target_resolution=(300, None))

clip.preview()