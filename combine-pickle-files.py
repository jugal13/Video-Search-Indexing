import pickle
import os
import glob
from collections import defaultdict

# combined = defaultdict(list)
# paths = set()
# for pkl_file in glob.glob(os.path.join('./hash-videos', '**/*.pkl'), recursive=True):
#     temp = pickle.load(open(pkl_file, 'rb'))
#     for entry in temp:
#         combined[entry['hash']].append((entry['frame_number'], entry['video_path']))
#         paths.add(entry['video_path'])

# print(paths)
# pickle.dump(combined, open('./hash-videos/combined.pkl', 'wb'))
def defaultdict_str():
    return defaultdict(str)

combined = defaultdict(defaultdict_str)
paths = set()

for pkl_file in glob.glob(os.path.join('./hash-videos', '**/*.pkl'), recursive=True):
    if pkl_file.endswith('combined.pkl'):
        continue
    with open(pkl_file, 'rb') as file:
        temp = pickle.load(file)
    
    # Check the type of temp - it should be a list of dictionaries
    print(f"Type of temp: {type(temp)}")
    
    if isinstance(temp, list):
        for entry in temp:
            # Confirm that each entry is a dictionary
            if isinstance(entry, dict):
                combined[entry['video_path']][entry['frame_number']] = entry['hash']
            else:
                print(f"Entry is not a dictionary: {entry}")
    else:
        print(f"Loaded data is not a list: {temp}")

# Since 'paths' set is not used elsewhere in the provided code, its print statement will just print an empty set
print(paths)

# Dumping the combined dictionary to a pickle file
with open('./hash-videos/path_to_frame_hash.pkl', 'wb') as out_file:
    pickle.dump(combined, out_file)