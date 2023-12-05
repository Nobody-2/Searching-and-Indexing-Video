import os
import subprocess

def get_video_duration(filename):
    """Get the duration of a video in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def create_clips(start_video_number, end_video_number):
    for video_number in range(start_video_number, end_video_number + 1):
        input_file = f"./Videos/video{video_number}.mp4"
        duration = get_video_duration(input_file)

        # Start and end times for clips
        start_time = 0
        clip_number = 1
        while start_time < duration:
            end_time = min(start_time + 30, duration)
            output_file = f"./Queries/video{video_number}_clip{clip_number}.mp4"

            ffmpeg_command = f"ffmpeg -ss {start_time} -i {input_file} -c copy -t {end_time - start_time} {output_file}"
            os.system(ffmpeg_command)

            print(f"Processed clip {clip_number} of {input_file}")

            start_time += 30
            clip_number += 1

# start and end video
start_video_number = 12
end_video_number = 20

create_clips(start_video_number, end_video_number)