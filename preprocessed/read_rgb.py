import numpy as np
import os

def read_rgb_file(file_path, width, height):
    frame_size = width * height * 3  # 3 bytes per pixel (RGB)

    with open(file_path, 'rb') as file:
        while True:
            # Read data for one frame
            frame_data = file.read(frame_size)
            if not frame_data:
                break  # Exit the loop if no more data is available

            # Convert the bytes into a 3D numpy array (height x width x RGB)
            frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((height, width, 3))

            yield frame

def read_frame(file_path):
    width, height = 352, 288

    concatenated_frames = []

    for frame in read_rgb_file(file_path, width, height):
        # Process each frame here
        # For example, display the frame or perform image processing
        concatenated_frames.append(frame)
    
    return concatenated_frames

def read_first_and_last_frame(file_path, width=352, height=288):
    frame_size = width * height * 3
    with open(file_path, 'rb') as file:
        # Get the total file size
        file.seek(0, os.SEEK_END)
        total_file_size = file.tell()

        # Calculate the total number of frames
        total_frames = total_file_size // frame_size

        # Read the first frame
        file.seek(0)
        first_frame_data = file.read(frame_size)
        first_frame = np.frombuffer(first_frame_data, dtype=np.uint8).reshape((height, width, 3))

        # Seek to the last frame
        file.seek(-frame_size, os.SEEK_END)
        last_frame_data = file.read(frame_size)
        last_frame = np.frombuffer(last_frame_data, dtype=np.uint8).reshape((height, width, 3))

        return first_frame, last_frame, total_frames
    
def read_rgb_custom_start_end(file_path, start_frame, end_frame, width=352, height=288):
    frame_size = width * height * 3  # 3 bytes per pixel (RGB)

    with open(file_path, 'rb') as file:
        # Skip frames until the start frame
        file.seek(frame_size * start_frame)

        for frame_num in range(start_frame, end_frame + 1):
            # Read data for one frame
            frame_data = file.read(frame_size)
            if not frame_data:
                break  # Exit the loop if no more data is available

            # Convert the bytes into a 3D numpy array (height x width x RGB)
            frame = np.frombuffer(frame_data, dtype=np.uint8).reshape((height, width, 3))
            yield frame

def cut_rgb_video(input_file_path, output_file_path, start_frame, end_frame):
    width, height = 352, 288  # Frame dimensions

    with open(output_file_path, 'wb') as output_file:
        for frame in read_rgb_custom_start_end(input_file_path, start_frame, end_frame, width, height):
            # Write each frame to the output file
            frame_bytes = frame.tobytes()
            output_file.write(frame_bytes)
