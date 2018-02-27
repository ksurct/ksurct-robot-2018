# This is the script to be ran of the rasberry pi
# after stream.sh is started on the basestation

rm -f fifo.500
mkfifo fifo.500
cat fifo.500 | nc.traditional -b 129.130.46.186 9001 &
/opt/vc/bin/raspivid -o fifo.500 -t 0 -b 1000000
rm fifo.500