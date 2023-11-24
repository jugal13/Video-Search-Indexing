import os
import glob
import pandas as pd
import pickle
import numpy as np

from Y_values_to_string import concatenate_y_values
from get_hash import generate_frame_hash
# from video_database import connect_to_mongo_server, find_by_hash, store_video_data
from read_rgb import read_frame

def train(mp4_file, collection):
    # first_file_processed = True
    # for mp4_file in glob.glob(os.path.join(root, '**/*.rgb'), recursive=True):

    print(f'Processing file {mp4_file}')
    y_values = read_frame(mp4_file)
    print('Y values genrated')
    records = []
    for frame_num, y in enumerate(y_values):
        if frame_num % 1000 == 0: 
            print(f'{frame_num} frames processed')
        record = {
            'hash': generate_frame_hash(y),
            'frame_number': frame_num,
            'video_path': mp4_file
        }
        records.append(record)
    print('Hash values generated')
    pickle.dump(records, open(f'./hash-values/{mp4_file.split("/")[-1][:-4]}.pkl', 'wb'))
        # store_video_data(col=collection, records=records)

        
        # # Convert records to DataFrame
        # df = pd.DataFrame(records)

        # # Write DataFrame to CSV
        # if first_file_processed:
        #     df.to_csv(output_file, mode='w', header=True, index=False)
        #     first_file_processed = False
        # else:
        #     df.to_csv(output_file, mode='a', header=False, index=False)

def main():
    # client = connect_to_mongo_server()
    # print('Connected to MongoDB')
    # db = client["VideoSearchIndexing"]
    # collection = db["VideoHash"]
    # collection.drop()
    video_dir = '/Users/sanjay/Downloads/video1.rgb'
    train(video_dir, 'collection')
    # client.close()

if __name__ == '__main__':
    main()

