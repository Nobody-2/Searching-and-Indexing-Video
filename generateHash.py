import json
from HashVideo import hash_videos

# USE THIS is you want to regenerate the video hash map, for example change the hash size or hash function

video_files = [f"./Videos/video{i}.mp4" for i in range(1, 21)]
# video_files = ["./Videos/video2.mp4"]
hash_tables_all = hash_videos(video_files, frame_step=1, hash_size=16)
with open("my_dict_new.json", "w") as f:
    json.dump(hash_tables_all, f)
