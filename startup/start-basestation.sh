#lxterminal --title="Client" -e 'bash -c "cd ~/Desktop/Mercury2018 && source venv/bin/activate && cd ksurct-robot-2018 && python Client.py;bash"'
#lxterminal --title="Stream" -e 'bash -c "cd ~/Desktop/Mercury2018 && cd ksurct-robot-2018/startup && ./stream.sh;bash"'
#these need to run in parallel, they run in series now

lxterminal --title="Client" -e 'bash -c "cd ~/Desktop/Mercury2018 && source venv/bin/activate && cd ksurct-robot-2018 && python Client.py;bash"' & lxterminal --title="Stream" -e 'bash -c "cd ~/Desktop/Mercury2018 && cd ksurct-robot-2018/startup && ./stream.sh;bash"'