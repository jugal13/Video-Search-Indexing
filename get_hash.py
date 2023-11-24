import hashlib
import numpy as np

def generate_frame_hash(y_channel_data):
    # Convert Y channel data to string
    # y_channel_string = ''.join(map(str, y_channel_data))
    

    hash_object = hashlib.sha256()
    y_bytes = y_channel_data.tobytes()

    # hash_object.update(y_channel_string.encode())
    hash_object.update(y_bytes)
    frame_hash = hash_object.hexdigest()

    return frame_hash

# y_channel_data = [123, 45, 67, 89, 33]
# frame_hash = generate_frame_hash(y_channel_data)
# print(frame_hash)