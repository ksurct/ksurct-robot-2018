# This receives the video stream from the pi when the pi is running send_video_stream.sh
# Run this script on the desktop to receive video
# Change 8001 to the port number desired for the stream to come across from the pi.

nc -l 8001  | mplayer -fps 60 -cache 2048 -
