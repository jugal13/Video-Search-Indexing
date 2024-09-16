from read_rgb import read_rgb_file
import numpy as np
import time

from generate_hash import train

def generate_hash_for_frame_diff(src_path):
    train(src_path)

def determine_threshold(file_path):
    width, height = 352, 288
    frame_number = 0
    frame_diff_values = []

    prev_frame = None

    for frame in read_rgb_file(file_path, width, height):
        frame_number += 1

        if prev_frame is not None:
            # Compute the absolute difference between frames
            frame_diff = np.sum(np.abs(frame - prev_frame))
            frame_diff_values.append(frame_diff)

        prev_frame = frame

    # Calculate the standard deviation of frame differences
    std_dev = np.std(frame_diff_values)

    # Set the threshold as a multiple of the standard deviation
    threshold = 2.0 * std_dev

    return threshold




def shot_detection(file_path, threshold):
    width, height = 352, 288

    prev_frame = None
    shot_detected = False
    frame_number = 0
    num_shots = 0

    for frame in read_rgb_file(file_path, width, height):
        frame_number += 1
        if prev_frame is not None:
            # Compute the absolute difference between frames
            frame_diff = np.sum(np.abs(frame - prev_frame))
            #print("frame difference: ",frame_diff)
            # Check if the frame difference exceeds the threshold
            if frame_diff > threshold:
                num_shots += 1
                if not shot_detected:
                    #print("Shot detected at frame ", frame_number)
                    shot_detected = True
            else:
                shot_detected = False

        prev_frame = frame

    print("Shot detection process completed.")
    print("Number of frames: ", frame_number)
    print("Number of shots: ", num_shots)

#shot_detection('dataset/queries/video1_1.rgb', 100000000)

our_threshold = 50000000
# Example usage to determine threshold
video_path = 'dataset/queries/video1_1.rgb'
print(video_path)
threshold = determine_threshold(video_path)
print(f"Recommended Threshold: {threshold}")
start_time = time.time()
shot_detection('dataset/queries/video1_1.rgb', threshold)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to execute the code: {elapsed_time} seconds")
shot_detection('dataset/queries/video1_1.rgb', our_threshold)

video_path = 'dataset/queries/video2_1.rgb'
print(video_path)
threshold = determine_threshold(video_path)
print(f"Recommended Threshold: {threshold}")
shot_detection('dataset/queries/video2_1.rgb', threshold)
shot_detection('dataset/queries/video2_1.rgb', our_threshold)

video_path = 'dataset/queries/video3_1.rgb'
print(video_path)
threshold = determine_threshold(video_path)
print(f"Recommended Threshold: {threshold}")
shot_detection(video_path, threshold)
shot_detection(video_path, our_threshold)

video_path = 'dataset/queries/video4_1.rgb'
print(video_path)
threshold = determine_threshold(video_path)
print(f"Recommended Threshold: {threshold}")
shot_detection(video_path, threshold)
shot_detection(video_path, our_threshold)

video_path = 'dataset/queries/video5_1.rgb'
print(video_path)
threshold = determine_threshold(video_path)
print(f"Recommended Threshold: {threshold}")
shot_detection(video_path, threshold)
shot_detection(video_path, our_threshold)