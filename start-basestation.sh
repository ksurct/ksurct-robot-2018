#lxterminal --title="Client" -e 'bash -c "cd ~/Desktop/Mercury2018 && source venv/bin/activate && cd ksurct-robot-2018 && python Client.py;bash"'
#lxterminal --title="Stream" -e 'bash -c "cd ~/Desktop/Mercury2018 && cd ksurct-robot-2018/startup && ./stream.sh;bash"'

lxterminal --title="Client" -e 'bash -c "cd ~/Desktop/Mercury2018/ksurct-robot-2018 && source venv/bin/activate && python Client.py;bash"' & lxterminal --title="Stream" -e 'bash -c "~/Desktop/Mercury2018/ksurct-robot-2018/video_stream/recv_video_stream.sh;bash"'
