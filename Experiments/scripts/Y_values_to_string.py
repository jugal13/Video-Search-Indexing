#import cv2
import os

def concatenate_y_values(video_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Get the frames per second (fps) of the input video
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Counter for frames
    frame_count = 0

    # List to store concatenated Y values for each frame
    concatenated_y_values = []

    # Loop through each frame in the video
    while True:
        # Read the next frame
        ret, frame = video_capture.read()

        # Break the loop if we have reached the end of the video
        if not ret:
            break

        # Convert the frame to YUV color space
        yuv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)

        # Extract the Y component (luminance)
        y_component = yuv_frame[:, :, 0]

        # Concatenate Y values into a single string for the frame
        y_values_string = "".join(map(str, y_component.flatten()))
        concatenated_y_values.append(y_values_string)

        frame_count += 1

    # Release the video capture object
    video_capture.release()

    return concatenated_y_values

# Specify the path to the video file
video_path = "video1.mp4"

# Call the function to concatenate Y values
concatenated_y_values = concatenate_y_values(video_path)

# Print the first 300 characters of each concatenated Y values string
for i, y_values in enumerate(concatenated_y_values):
    #print("Frame : ",i+1)
    print(f"Frame {i + 1} Y values: {y_values[:30]}")
