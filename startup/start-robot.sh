# Sends video or something

lxterminal --title="Main" -e 'bash -c "cd ~/Desktop/Mercury2018 && source venv/bin/activate && cd ksurct-robot-2018 && python Main.py;bash"' & lxterminal --title="Video" -e 'bash -c "cd ~/Desktop/Mercury2018 && cd ksurct-robot-2018/startup && ./video.sh;bash"'