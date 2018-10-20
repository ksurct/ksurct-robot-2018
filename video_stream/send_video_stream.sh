# This is the script to be ran of the rasberry pi
# after recv_video_stream.sh is started on the basestation

rm -f fifo.500
mkfifo fifo.500
cat fifo.500 | nc.traditional -b 10.243.188.212 8001 &
/opt/vc/bin/raspivid -hf -vf -o fifo.500 -t 0 -b 1000000
rm fifo.500
