# ksurct-robot-2018

## Quick start guide

1. Make sure python 3.5+ is installed

2. Use the raspi-config gui to enable the Camera SSH, SPI, and I2C
```
sudo raspi-config
```
3. Clone this repository
```
git clone https://github.com/ksurct/ksurct-robot-2018.git
```
4. Create a virtual environment with virtualenv
```
virtualenv -p python3 venv
```
5. Activate the virtual environment, you will have to do this everytime you want to use the installed packages for the robot
```
source venv/bin/activate
```
6. Install the required python packages
```
pip install -r pi-requirements.txt
```
