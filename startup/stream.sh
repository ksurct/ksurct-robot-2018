# This receives the video stream from the pi when the pi is running video.sh
# Run this script on the desktop to receive video
# Change 9001 to the port number desired for the stream to come across from the pi.

nc -l 9001  | mplayer -fps 60 -cache 1024 -
