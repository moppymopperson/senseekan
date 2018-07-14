# Senseekan

## Setting up on Docker
The easiest way to run Senseekan is with Docker Compose. All you need to do is clone the repository and then `docker-compose up` from the root directory. The compose file will setup both the bluetooth wiimote server and the webcam server to run automatically on startup. This way, Senseekan will continually try to connect to wiimotes and webcams any time that it has power.

