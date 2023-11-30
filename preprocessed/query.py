import time
import pickle
import numpy as np
from get_hash import generate_frame_hash
from read_rgb import read_first_and_last_frame, read_frame, read_rgb_file


def query_by_first_or_last_frame(video_path, hash_values):
    # client = connect_to_mongo_server()
    # db = client["VideoSearchIndexing"]
    # collection = db["VideoHash"]
    # collection.drop()
    # result = collection.find({})
    # result_pair = [(str(record['hash'])) for record in result]
    # print(result_pair)
    # print('Connected to MongoDB')

    first_frame, last_frame, video_length = read_first_and_last_frame(video_path)
    first_frame_hash, last_frame_hash = generate_frame_hash(first_frame), generate_frame_hash(last_frame)
    first_frame_results, last_frame_results = hash_values[first_frame_hash], hash_values[last_frame_hash]

    if len(first_frame_results) == 1:
        print(first_frame_results)
        print(f'{(first_frame_results[0][0] / 30) // 60} mins {(first_frame_results[0][0] / 30) % 60} seconds')
        return

    elif len(last_frame_results) == 1:
        # path_to_hash = pickle.load(open('./hash-videos/path_to_frame_hash.pkl', 'rb'))
        print(last_frame_results[0][0] - video_length, last_frame_results[0][1])
        print(
            f'{(last_frame_results[0][0] - video_length / 30) // 60} mins {(last_frame_results[0][0] - video_length / 30) % 60} seconds')
        return
    # client.close()
    else:
        print('Still implementing')


def query_frame_diff(file_path, diff_hash_values):
    frame_diff_concatenated = []
    width, height = 352, 288
    prev_frame = None
    shot_detected = False
    idx = 0
    num_shots = 0
    for frame in read_rgb_file(file_path, width, height):
        idx += 1
        if prev_frame is not None:
            # Compute the absolute difference between frames
            frame_diff = np.abs(frame - prev_frame)
            frame_diff_sum = np.sum(frame_diff)
            if frame_diff_sum > 0:
                diff_hash = generate_frame_hash(frame_diff)
                res = diff_hash_values[diff_hash]
                print(res)
                if (len(res)) == 1:
                    # print(frame_number)
                    first_frame = res[0][0] - idx + 2
                    print(f'Query found in Video {res[0][1]} at index {(first_frame / 30) // 60} mins {(first_frame / 30) % 60} seconds')
                    return first_frame
        prev_frame = frame


if __name__ == '__main__':
    video_path = '/Users/pratheekshaprasad/PycharmProjects/VideoIndexer/video-search-indexing/dataset/queries/video11_1.rgb'
    pickle_path = './hash-videos/combined.pkl'
    hash_values = pickle.load(open(pickle_path, 'rb'))  # 0.4s
    start_time = time.time()
    query_by_first_or_last_frame(video_path, hash_values)  # 0.003s
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to execute the code: {elapsed_time} seconds")

    diff_pickle_path = './hash-diff-videos/combined.pkl'
    diff_hash_values = pickle.load(open(diff_pickle_path, 'rb'))
    start_time = time.time()
    query_frame_diff(video_path, diff_hash_values)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to execute the code: {elapsed_time} seconds")