import os
import sys

from HashVideo import hash_videos

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import mixer

import numpy as np
import imagehash
import time as tmclear
import json
import hashlib
from scipy import stats
from sklearn.cluster import DBSCAN
import time as tm

import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from OnlyPlayVideo import playVideo


path_query = ""  # ./Queries/video1_1.mp4
mode_query = ""  # simple, debug

# pass as CLI arguments : python Main.py ./Queries/video1_1.mp4 simple


def main():
    global path_query
    if len(sys.argv) == 3:
        path_query = sys.argv[1]
        # print(f"Path query: {path_query}")

        global mode_query
        mode_query = sys.argv[2]  # simple / split
        # print(f"Mode: {mode_query}")

    elif len(sys.argv) == 2:
        path_query = sys.argv[1]
        # print(f"Path query: {path_query}")


if __name__ == "__main__":
    main()

# USE THIS is you want to regenerate the video hash map, for example change the hash size or hash function

# video_files = [f"./Videos/video{i}.mp4" for i in range(1, 21)]
# hash_tables_all = hash_videos(video_files, frame_step=1, hash_size=16)
# with open("Combined_dict_win.json", "w") as f:
#     json.dump(hash_tables_all, f)
# os.remove("tempFrameFile.bmp")


# path_query = "./Queries/video8_1.mp4"

with open("Combined_dict.json") as f:
    hash_table_all = json.load(f)

start_time = tm.time()

# hash_table_all = {}
# RGB Hash
# video_files = [f"./Videos/RGB_Files/video{i}.rgb" for i in range(1, 2)]
# hash_table_all_temp = hash_videos(video_files, frame_step=1, hash_size=16)
# for file, table in hash_table_all_temp.items():
#     hash_table_all[file] = table
# with open("my_dict_rgb.json", "w") as f:
#     json.dump(hash_table_all, f)

Covered_frames = []
frameno = 0
savedframes = 0
cap1 = cv2.VideoCapture(path_query)
if not cap1.isOpened():
    print("Cannot find / open file: " + path_query)
    sys.exit(1)
bufferName = "tempFrameFile.bmp"
time1 = cap1.get(cv2.CAP_PROP_POS_MSEC)
fps1 = cap1.get(cv2.CAP_PROP_FPS)
total_frames1 = cap1.get(cv2.CAP_PROP_FRAME_COUNT)
while True:
    ret, frame = cap1.read()
    if ret:
        # print("time stamp current frame:", frameno / fps1)
        cv2.imwrite(bufferName, frame)
        savedframes += 1
        temp = str(imagehash.phash(Image.open(bufferName), hash_size=16))
        # temp = hashlib.md5(Image.open(bufferName))
        if temp in hash_table_all:
            # print(
            #     "found frame in "
            #     + str(frameno)
            #     + " is in hash_table (original video) "
            #     + str(len(hash_table_all[temp]))
            #     + str(hash_table_all[temp])
            # )
            # Covered_frames += [hash_table_all[temp][i] - frameno for i in range(len(hash_table_all[temp]))]
            # if len(hash_table_all[temp]) < 20:
            arr = hash_table_all[temp]
            arr = [[ele[0], ele[1] - frameno] for ele in arr]
            Covered_frames += arr
            # print(frameno, Covered_frames)
    else:
        cap1.release()
        break
    frameno += 100
    cap1.set(cv2.CAP_PROP_POS_FRAMES, frameno)

# print(Covered_frames)

green_text = "\033[92m"
reset_text = "\033[0m"

print(green_text + "--- %s seconds ---" % (tm.time() - start_time) + reset_text)

# This part below should use the formatted code in HashVideo but some bug exist so please use above raw code

# start_time = tm.time()
# found_frames = search_query_video(path_query, hash_table_all)
# print("--- %s seconds ---" % (tm.time() - start_time))
# print("Found Frames:", found_frames)
#
# frames_flatted = frame_numbers = [original_frame_no for _, original_frame_no, _ in found_frames]


if not Covered_frames:
    print("No search matches found")
    sys.exit(1)


def most_frequent(List):
    unique, counts = np.unique(List, return_counts=True)
    index = np.argmax(counts)
    return unique[index]


Most_common_path = ""
Video_path_all = []

for each_frame in Covered_frames:
    Video_path_all.append(each_frame[0])
Most_common_path = most_frequent(Video_path_all)
Filtered_frames = []
for each_frame in Covered_frames:
    Filtered_frames.append(each_frame[1])

start_frame_arr = [arr[1] for arr in Covered_frames]
most_frequent_frame = most_frequent(start_frame_arr)
start_frame = round(most_frequent_frame / 30) * 30
print("start_frame", start_frame)

path_arr = [arr[0] for arr in Covered_frames if arr[1] == most_frequent_frame]
path_orig = most_frequent(path_arr)
print("Video matched to:" + path_orig)

#  BELOW ARE VIDEO PLAYER
window = tk.Tk()
window.title("Video Player")

# Set up the main and query videos
main_cap = cv2.VideoCapture(path_orig)
# main_player = MediaPlayer(path_orig)
main_cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

query_cap = cv2.VideoCapture(path_query)
# Get total number of frames and fps for both videos
total_frames_main = int(main_cap.get(cv2.CAP_PROP_FRAME_COUNT))
total_frames_query = int(query_cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps_main = main_cap.get(cv2.CAP_PROP_FPS)
fps_query = query_cap.get(cv2.CAP_PROP_FPS)

# Create labels on the window to display the videos
lbl_main_video = tk.Label(window)
lbl_main_video.grid(row=0, column=0)
lbl_query_video = tk.Label(window)
lbl_query_video.grid(row=0, column=1)

# Create progress bars
progress_main = ttk.Progressbar(
    window, length=200, mode="determinate", maximum=total_frames_main
)
progress_main.grid(row=2, column=0)
progress_query = ttk.Progressbar(
    window, length=200, mode="determinate", maximum=total_frames_query
)
progress_query.grid(row=2, column=1)

# Create labels to display current frame and timestamp
lbl_main_info = tk.Label(window, text="Frame: 0, Time: 0s")
lbl_main_info.grid(row=3, column=0)
lbl_query_info = tk.Label(window, text="Frame: 0, Time: 0s")
lbl_query_info.grid(row=3, column=1)


# This variable will hold the reference to the after event
after_id = None


def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}m {secs}s"


# Texts
lbl_video_source = tk.Label(window, text="Source Video: " + path_orig)
lbl_video_source.grid(row=4, column=0, columnspan=2)
query_start_time = 0  # Replace with actual start time in seconds
query_end_time = 0  # Replace with actual end time in seconds


lbl_query_times = tk.Label(
    window
    # ,
    # text=f"Query Start: {format_time(query_start_time)}, "
    # f"Query End: {format_time(query_end_time)}",
)
lbl_query_times.grid(row=5, column=0, columnspan=2)


def set_video_info(source_video_path, start_time, end_time):
    lbl_video_source.config(text=f"Source Video: {source_video_path}")
    # lbl_query_times.config(
    #     text=f"Query Start: {format_time(start_time)}, Query End: {format_time(end_time)}"
    # )


# Call this function when you have the details for the query clip
set_video_info(path_orig, query_start_time, query_end_time)

simple_start_time = 0


# Function to update the frames for both videos
def update_frames():
    global after_id
    global simple_start_time
    ret_main, frame_main = main_cap.read()
    ret_query, frame_query = query_cap.read()

    # Check if the query video has finished playing
    if not ret_query:
        # Reset the query video to the first frame and continue playing
        query_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret_query, frame_query = query_cap.read()

    # If the main video has finished playing, you might want to handle this as well
    if not ret_main:
        # Handle end of main video playback if necessary
        pass

    # Update progress bars and info labels for the main video
    current_frame_main = int(main_cap.get(cv2.CAP_PROP_POS_FRAMES))
    progress_main["value"] = current_frame_main
    time_main = current_frame_main / fps_main
    simple_start_time = time_main
    formatted_time_main = format_time(time_main)
    lbl_main_info.config(
        text=f"Frame: {current_frame_main}, Time: {formatted_time_main}"
    )

    # Update progress bars and info labels for the query video
    current_frame_query = int(query_cap.get(cv2.CAP_PROP_POS_FRAMES))
    progress_query["value"] = current_frame_query
    time_query = current_frame_query / fps_query
    formatted_time_query = format_time(time_query)
    lbl_query_info.config(
        text=f"Frame: {current_frame_query}, Time: {formatted_time_query}"
    )

    # Convert frames to PIL format and update the labels
    frame_main_rgb = cv2.cvtColor(frame_main, cv2.COLOR_BGR2RGB)
    frame_query_rgb = cv2.cvtColor(frame_query, cv2.COLOR_BGR2RGB)

    img_main = Image.fromarray(frame_main_rgb)
    img_query = Image.fromarray(frame_query_rgb)

    imgtk_main = ImageTk.PhotoImage(image=img_main)
    imgtk_query = ImageTk.PhotoImage(image=img_query)

    lbl_main_video.imgtk = imgtk_main
    lbl_query_video.imgtk = imgtk_query

    lbl_main_video.configure(image=imgtk_main)
    lbl_query_video.configure(image=imgtk_query)

    # Schedule the next frame update
    after_id = window.after(29, update_frames)


video_filename = path_orig.split("/")[-1]
audio_filename = video_filename.split(".")[0] + ".wav"
audio_path = "./Videos/Audios/" + audio_filename
# print(audio_path)


mixer.init()
mixer.music.load(audio_path)
mixer.pause()
paused = True
reset = True

wav_start = start_frame / 30
# print(wav_start)


# Control buttons
def play_videos():
    global paused
    global reset
    if reset:
        mixer.music.play()
        mixer.music.set_pos(wav_start)
        reset = False
        paused = False
    elif paused:
        mixer.music.unpause()
        paused = False
    global after_id
    if after_id is None:  # Start the update loop only if it's not already running
        update_frames()


def reset_videos():
    global after_id
    if after_id:
        window.after_cancel(after_id)  # Cancel the ongoing frame update loop
        after_id = None
    main_cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    query_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    progress_main["value"] = 0
    progress_query["value"] = 0
    lbl_main_info.config(text="Frame: 0, Time: 0s")
    lbl_query_info.config(text="Frame: 0, Time: 0s")
    global reset
    reset = True
    mixer.music.pause()
    global paused
    paused = True


def pause_videos():
    global after_id
    if after_id:
        window.after_cancel(after_id)  # Cancel the ongoing frame update loop
        after_id = None
    global paused
    paused = True
    mixer.music.pause()


btn_reset = ttk.Button(window, text="RESET", command=reset_videos)
btn_reset.grid(row=1, column=0)
btn_play = ttk.Button(window, text="PLAY", command=play_videos)
btn_play.grid(row=1, column=1)
btn_pause = ttk.Button(window, text="PAUSE", command=pause_videos)
btn_pause.grid(row=1, column=2)

if mode_query == "simple":
    update_frames()
    playVideo(path_orig, int(simple_start_time))

else:
    window.mainloop()
