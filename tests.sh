#!/bin/bash
PYTHON_PATH="/opt/homebrew/bin/python3"
# Loop through the video files from video1_1.mp4 to video12_1.mp4
for i in {1..11}
do
    # Execute the python script with each video file
    $PYTHON_PATH Main.py ./Queries/video${i}_1.mp4 simple
done
