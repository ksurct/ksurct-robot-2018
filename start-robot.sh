# Starts the python code and the video stream on the robot
# Currently doesn't work on pi because it can't open a display
# Error when run: (lxterminal:2268): Gtk-WARNING **: cannot open display:
lxterminal --title="Main" -e 'bash -c "cd ~/Desktop/Mercury2018/ksurct-robot-2018 && source venv/bin/activate && python Main.py;bash"' & lxterminal --title="Video stream" -e 'bash -c "~/Desktop/Mercury2018/ksurct-robot-2018/video_stream/send_video_stream.sh;bash"'