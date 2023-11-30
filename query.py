import time
import pickle
import numpy as np
import argparse
from get_hash import generate_frame_hash
from read_rgb import read_rgb_file


def convertFrameToMin(frame_number):
    return (frame_number / 30) // 60


def convertFrameToSec(frame_number):
    return (frame_number / 30) % 60


def query_frame_diff(file_path, hash_video_database):
    width, height = 352, 288
    prev_frame = None
    frame_idx = 0

    for frame in read_rgb_file(file_path, width, height):
        frame_idx += 1
        if prev_frame is not None:
            # Compute the absolute difference between frames
            frame_diff = np.abs(frame - prev_frame)
            # SAD of frame differences
            frame_diff_sum = np.sum(frame_diff)

            if frame_diff_sum > 0:
                diff_hash = generate_frame_hash(frame_diff)
                res = hash_video_database[diff_hash]
                if (len(res)) == 1:
                    video_path = res[0][1]
                    first_frame = res[0][0] - frame_idx + 2

                    return first_frame, video_path
        prev_frame = frame


# if __name__ == '__main__':

#     # if video path as cmd arg
#     parser = argparse.ArgumentParser(description='Query path.')
#     parser.add_argument(
#         '--query_path',
#         type=str,
#         help='Path to the video file'
#     )
#     args = parser.parse_args()
#     query_path = args.query_path

#     diff_pickle_path = './hash-diff-videos/combined.pkl'
#     diff_hash_values = pickle.load(open(diff_pickle_path, 'rb'))  # 0.4s

#     start_time = time.time()
#     first_frame, video_path = query_frame_diff(
#         query_path,
#         diff_hash_values
#     )  # 0.003s
#     end_time = time.time()

#     elapsed_time = end_time - start_time
#     print(f"Time taken to query: {elapsed_time} seconds")
