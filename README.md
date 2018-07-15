# Senseekan

## Setting up on Docker
The easiest way to run Senseekan is with Docker Compose. All you need to do is clone the repository and then run `docker-compose up` from the root directory. The compose file will setup a group of containers running all the softare in the proper environment for each. 

## Setup Instructions
1. Install docker on your RPi
  - You'll find various sets of instructions on the web. I used this `curl -sSL https://get.docker.com | sh`
2. Install `docker-compose` on your RPi
  - There are many ways, but `pip install docker-compose` is by far the easiest
3. Clone this repository to someplace on your RPi
  - `git clone https://github.com/moppymopperson/senseekan`
  - `cd senseekan`
3. Connect your webcam or Theta S to the RPi via USB
  - If you're using a Theta S, make sure it is `Live` mode *before* goint to step 4
4. Start the containers with docker-compose
  - `docker-compose up -d`
  - The `-d` tag (detach) makes everything run in the background
  - You're all set now. The containers should run automatically anytime you power on your RPi
5. From a browser, connect to your raspberrypi via IP address or hostname
  - Probably something like `http://raspberypi.local` or `http://192.168.2.1`

## Running Automatically on Startup
Docker has a convenient `--restart always` flag the I tried to use to make the containers restart on boot, but it happens too early in the boot process and causes some problems. A better solution is to setup Senseekan as a service and let `systemd` handle it for you.
1. Update the working directory in `senseekan.service` to the directory you have cloned Senseekan to
2. Copy the `senseekan.service` file to /etc/systemd/system/senseekan.service
3. Run `sudo systemctl enable senseekan` to register the new service to run at startup
4. Either reboot or run `sudo systemctl start` to get the new service running
  - After reboot you can check that it worked by running `docker ps` to see if all the containers are up

## Composition
There are 4 containers involved in this app.
1. senseekan
  - Contains Python code that connects to wiimotes via bluetooth and turns mototrs attached to pins 31, 33, 35, and 37
2. streamer
  - Contains `mjpg-streamer`. Captures frames from the webcam or Theta S and streams them over HTTP
3. web
  - Contains a simple HTTP server that provides the javascript and http files that are displayed when you visit your RPi's website
  - For the Theta S, projection of the dual fish eye image from the camera happens in the scripts provided by this server
4. nginxproxy
  - Routes requests to the appropriate container and adds headers needed to avoid CORS problems when rendering images

## Troubleshooting
If the video doesn't show up, it's likely the camera was not in `Live` mode when the streamer container started. Ensure the camera is in Live mode and then run `docker-compose restart streamer`

## Theta S Projection Mapping
The Theta S provides images in a dual fish eye format. To display this properly on a phone or computer, we need to project images onto the inside of sphere. The code from this is in the `/web` directory. It uses a modified version of Ricoh's `thetaview.js`. Typically `thetaview.js` uses a `<video>` tag, but here we only have access to mjpeg video, which cannot be rendered in a video tag. To get around this, I created a version which draws the most recent video frame to `canvas` element, registers that element as a texture for projection, and then forces an update on each frame. It's a little resource intensive, but it works well enough.
