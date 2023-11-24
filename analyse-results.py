import pickle
import pandas as pd

from collections import defaultdict
from get_hash import generate_frame_hash
from read_rgb import read_frame

hash_values = pickle.load(open('./hash-values/video1.pkl', 'rb'))

def test(video_path, hash_values):
    video_reader = read_frame()(video_path)

    for frame in video_reader:
        frame_hash = generate_frame_hash(frame)
        for entry in hash_values:
            if frame_hash == entry['hash']:
                print(entry)
                return

print(test('/Users/sanjay/Downloads/576_final_PA/Queries/video1_1.rgb', hash_values))