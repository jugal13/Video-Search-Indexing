import os
import glob
import pandas as pd
import cv2
import time
import pickle

# from Y_values_to_string import concatenate_y_values
from get_hash import generate_frame_hash
# from video_database import connect_to_mongo_server, find_by_hash, store_video_data
from read_rgb import read_first_and_last_frame



def test(video_path, hash_values):
    
    # print('Hash Generated')
    # frame_number, video_path = find_by_hash(col=collection, hash_value=frame_hash)
    # print('Query Ran')



    return 


def main():
    start_time = time.time()
    # client = connect_to_mongo_server()
    # db = client["VideoSearchIndexing"]
    # collection = db["VideoHash"]
    # collection.drop()
    # result = collection.find({})
    # result_pair = [(str(record['hash'])) for record in result]
    # print(result_pair)
    # print('Connected to MongoDB')
    video_path = '/Users/sanjay/Downloads/576_final_PA/Queries/video1_1.rgb'
    pickle_path = './hash-videos/combined.pkl'
    hash_values = pickle.load(open(pickle_path, 'wb'))
    first_frame, last_frame, video_length = read_first_and_last_frame(video_path)

    first_frame_hash, last_frame_hash = generate_frame_hash(first_frame), generate_frame_hash(last_frame)
    

    first_frame_results, last_frame_results = hash_values[first_frame_hash], hash_values[last_frame_hash]



    if len(first_frame_results) == 1:
        end_time = time.time()
        print(f'Time taken: {end_time - start_time}')
        print(first_frame_results[0], first_frame_results[1])
        return
    
    elif len(last_frame_results) == 1:
        # path_to_hash = pickle.load(open('./hash-videos/path_to_frame_hash.pkl', 'rb'))
        end_time = time.time()
        print(f'Time taken: {end_time - start_time}')
        print(last_frame_results[0] - video_length, last_frame_results[1])
        return
    # client.close()
    else:
        print('Still implementing')


if __name__ == '__main__':
    main()
