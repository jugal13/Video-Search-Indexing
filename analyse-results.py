import pickle
import pandas as pd
import os
import glob

from collections import defaultdict
from get_hash import generate_frame_hash
from read_rgb import read_frame


def test(video_path, hash_values):
    video_reader = read_frame()(video_path)

    for frame in video_reader:
        frame_hash = generate_frame_hash(frame)
        for entry in hash_values:
            if frame_hash == entry['hash']:
                print(entry)
                return

def split_into_continuous_lists(numbers):
    continuous_lists = []
    current_list = []

    for i, num in enumerate(numbers):
        if i == 0 or num == numbers[i - 1] + 1:
            current_list.append(num)
        else:
            continuous_lists.append(current_list)
            current_list = [num]
    
    if current_list:
        continuous_lists.append(current_list)
    
    return continuous_lists

def check_duplicates(root):
    for pkl_file in glob.glob(os.path.join(root, '**/*.pkl'), recursive=True):
        if pkl_file.endswith('combined.pkl') or pkl_file.endswith('path_to_frame_hash.pkl'):
            continue
        hash_values = pickle.load(open(pkl_file, 'rb'))
        hash_set = defaultdict(list)

        for entry in hash_values:
            hash_set[entry['hash']].append(entry['frame_number'])

        print_flag = False

        for h, frames in hash_set.items():
            if len(frames) > 1:
                continuous_frames = split_into_continuous_lists(sorted(frames))
                if continuous_frames:
                    if not print_flag:
                        print(f'Duplicates found in {pkl_file}: ')
                        print_flag = True
                    for frame_list in continuous_frames:
                        if len(frame_list) > 1:
                            print(f'Continuous frames with same hash: {frame_list}, Length: {len(frame_list)}')
        print()
    return

def check_duplicates_pkl(pkl_file):
    hash_values = pickle.load(open(pkl_file, 'rb'))
    hash_set = defaultdict(list)

    for entry in hash_values:
        hash_set[entry['hash']].append(entry['frame_number'])

    print_flag = False
    for h, f in hash_set.items():
        if len(f) > 1:
            if not print_flag:
                print(f'Duplicates found in {pkl_file}: ')
                print_flag = True
            print(f'Frames with same values: {f}')
    print()


def main():

    check_duplicates('./hash-videos/')

    # Code to run query
    # hash_values = pickle.load(open('./hash-values/video1.pkl', 'rb'))
    # print(test('/Users/sanjay/Downloads/576_final_PA/Queries/video1_1.rgb', hash_values))

if __name__ == '__main__':
    main()