#! /bin/bash

# This script creates a tmux session with two split windows and then
# executes the python script to listen to the LORA signal.

NAME='lora_ses'
LOC='/home/pi/Desktop/Lora_dalykai/LORA_PI_RX.py'
tmux new-session -s "$NAME" -d
tmux split-window -t "$NAME" -h -p 50
tmux send -t "$NAME.0" "python3 $LOC" ENTER
