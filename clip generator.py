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

def create_clips_and_analyze(start_video_number, end_video_number, frame_rate):
    for video_number in range(start_video_number, end_video_number + 1):
        input_file = f"./Videos/video{video_number}.mp4"
        duration = get_video_duration(input_file)

        start_time = 0
        clip_number = 1
        while start_time < duration:
            end_time = min(start_time + 30, duration)
            output_file = f"./Queries/video{video_number}_clip{clip_number}.mp4"

            # Calculate the start and end frame for this clip
            start_frame = int(start_time * frame_rate)
            end_frame = int(end_time * frame_rate) - 1  # -1 because frames are zero-indexed

            # ffmpeg_command = f"ffmpeg -ss {start_time} -i {input_file} -c copy -t {end_time - start_time} {output_file}"
            ffmpeg_command = f"ffmpeg -ss {start_time} -i {input_file} -c copy -t {end_time - start_time} {output_file} >NUL 2>&1"
            os.system(ffmpeg_command)

            print(f"Clip {clip_number} of {input_file} generated.")
            print(f"Clip starts at frame: {start_frame} and ends at frame: {end_frame}")

            # Call your program with the generated clip
            program_command = f"python Main.py {output_file} s"
            process = subprocess.Popen(program_command, shell=True, stdout=subprocess.PIPE)
            program_output = process.communicate()[0].decode().strip()

            print(f"Your program detected start frame: {program_output}")
            print("===================")
            start_time += 30
            clip_number += 1

# Define the start and end of your video range and the frame rate of the videos
start_video_number = 12
end_video_number = 20
frame_rate = 30  # Update this with the actual frame rate of your videos

create_clips_and_analyze(start_video_number, end_video_number, frame_rate)