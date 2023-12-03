import cv2
import json
from PIL import Image
import imagehash
import time as tm

def hash_frame(frame, hash_size=16):
    """
    Hash a single frame using perceptual hash.

    :param frame: The frame to be hashed.
    :param hash_size: The size of the hash.
    :return: Hash of the frame.
    """
    buffer_name = 'tempFrameFile.bmp'
    cv2.imwrite(buffer_name, frame)
    return str(imagehash.phash(Image.open(buffer_name), hash_size=hash_size))
    # return hashlib.md5(Image.open(buffer_name).encode())

def process_video(video_path, frame_step=10, hash_size=16):
    """
    Process a video file to create a hash table of its frames.

    :param video_path: Path to the video file.
    :param frame_step: The number of frames to skip for each hash.
    :param hash_size: The size of the hash.
    :return: A dictionary where keys are hashes and values are lists of frame numbers.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")

    hash_table = {}
    frameno = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_hash = hash_frame(frame, hash_size=hash_size)
        hash_table.setdefault(frame_hash, []).append(frameno)

        frameno += frame_step
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameno)

    cap.release()
    return hash_table

def hash_videos(video_paths, frame_step=10, hash_size=16):
    """
    Process multiple video files to create hash tables for each.

    :param video_paths: List of paths to the video files.
    :param frame_step: The number of frames to skip for each hash.
    :param hash_size: The size of the hash.
    :return: A dictionary where keys are video paths and values are the corresponding hash tables.
    """
    hash_tables = {}
    for path in video_paths:
        print("Processing video " + str(path))
        try:
            hash_tables[path] = process_video(path, frame_step, hash_size)
            print("Finished")
        except IOError as e:
            print(f"Error processing {path}: {e}")

    return hash_tables

def search_query_video(query_video_path, hash_table_all, frame_step=1, hash_size=16):
    """
    Search for matches of the query video in all provided hash tables.

    :param query_video_path: Path to the query video file.
    :param hash_table_all: A dictionary containing hash tables for all original videos.
    :param frame_step: The number of frames to skip for each hash.
    :param hash_size: The size of the hash.
    :return: A list of tuples, each containing the original video path, the frame number in the original video, and the frame number in the query video.
    """
    search_results = []
    cap = cv2.VideoCapture(query_video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open query video file: {query_video_path}")

    frameno = 0
    buffer_name = 'tempFrameFile.bmp'

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imwrite(buffer_name, frame)
        frame_hash = str(imagehash.phash(Image.open(buffer_name), hash_size=hash_size))

        for original_video, hash_table in hash_table_all.items():
            if frame_hash in hash_table:
                for original_frame_no in hash_table[frame_hash]:
                    print(f"Found match: Query frame {frameno} in '{query_video_path}' matches frame {original_frame_no} in '{original_video}'")
                    search_results.append((original_video, original_frame_no, frameno))

        frameno += frame_step
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameno)

    cap.release()
    return search_results
