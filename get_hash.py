import hashlib


def generate_frame_hash(channel_data):
    # SHA256 Hash of RGB channel data
    hash_object = hashlib.sha256()
    # Convert to bytes
    channel_bytes = channel_data.tobytes()

    hash_object.update(channel_bytes)
    frame_hash = hash_object.hexdigest()

    return frame_hash
