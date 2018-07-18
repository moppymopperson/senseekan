FROM resin/rpi-raspbian:latest

RUN apt-get update && apt-get -y upgrade

# Needed for controlling GPIO from Python
RUN apt-get install python-dev python-rpi.gpio

# Neede for Bluetooth interfacing with the wiimote
RUN apt-get install pi-bluetooth python-cwiid
