@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Loop from 1 to 11
FOR /L %%G IN (1,1,11) DO (
    REM Execute the Python script with each video file
    python Main.py ./Queries/video%%G_1.mp4 simple
)

ENDLOCAL
