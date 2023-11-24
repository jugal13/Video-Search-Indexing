import os
import glob
import pandas as pd
import cv2
import time

from Y_values_to_string import concatenate_y_values
from get_hash import generate_frame_hash
from video_database import connect_to_mongo_server, find_by_hash, store_video_data



def test(video_path, collection):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    ret, frame = video_capture.read()

    # Convert the frame to YUV color space
    yuv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)[:, :, 0]

    # Extract the Y component (luminance)
    y_component = yuv_frame

    # Concatenate Y values into a single string for the frame
    y_values_string = "".join(map(str, y_component.flatten()))

    frame_hash = generate_frame_hash(y_values_string)
    print('Hash Generated')
    frame_number, video_path = find_by_hash(col=collection, hash_value=frame_hash)
    print('Query Ran')

    # Release the video capture object
    video_capture.release()

    return frame_number, video_path



def main():
    start_time = time.time()
    client = connect_to_mongo_server()
    db = client["VideoSearchIndexing"]
    collection = db["VideoHash"]
    # collection.drop()
    result = collection.find({})
    result_pair = [(str(record['hash'])) for record in result]
    print(result_pair)
    print('Connected to MongoDB')
    video_path = '/Users/sanjay/Downloads/576_final_PA/Queries/video1_1.mp4'
    frame_num, result_path = test(video_path, collection)
    end_time = time.time()
    print(f'Time taken: {end_time - start_time}')
    print(frame_num, result_path)
    client.close()

if __name__ == '__main__':
    main()
