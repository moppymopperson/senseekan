# Senseekan

## Setting up on Docker
The easiest way to run Senseekan is with Docker Compose. All you need to do is clone the repository and then run `docker-compose up` from the root directory. The compose file will setup a group of containers running all the softare in the proper environment for each. It will also configure the containers to restart on boot, so all you need to do is give your RPi power and it should automatically search for wiimotes and webcames.

## Setup Instructions
1. Install docker on your RPi
  - You'll find various sets of instructions on the web. I used this `curl -sSL https://get.docker.com | sh`
2. Install `docker-compose` on your RPi
  - There are many ways, but `sudo pip install docker-compose` is by far the easiest (sudo is necessary!)
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
  - If you want to see the raw, unprojected video stream (like when using a standard webcam instead of a Theta S), you can visit `http://yourhostname.local/webcam`
  - You can also get a single frame by going to `http://yourhostname.local/frame`

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
If your wiimote does not connect, odds are that it is not the right kind. In 2016 when this project was conceived, newer models weren't compatible with `cwiid` (the package Senseekan uses). That may have changed since then, but I haven't tested with any but the old model wiimote. When you build the docker image, it automatically fetches the latest version of cwiid, so if there have been any updates they should take effect. 

## Theta S Projection Mapping
The Theta S provides images in a dual fish eye format. To display this properly on a phone or computer, we need to project images onto the inside of sphere. The code from this is in the `/web` directory. It uses a modified version of Ricoh's `thetaview.js`. Typically `thetaview.js` uses a `<video>` tag, but here we only have access to mjpeg video, which cannot be rendered in a video tag. To get around this, I created a version which draws the most recent video frame to `canvas` element, registers that element as a texture for projection, and then forces an update on each frame. It's a little resource intensive, but it works well enough.

## Running in the wild
You probably won't have access to a wireless network when using Senseekan, so the best solution is to setup your RPi to act as an access point for a local network. You can then connect to your RPi's wifi network from your phone or computer and access the server as ususal.

There are a number of guides on how to do this. The official docs are out of date and don't work. I've found the easiest solution is this script.
https://gist.github.com/Lewiscowles1986/fecd4de0b45b2029c390

You may find, as I did, that the RPi is pretty terrible access point, and cannot stream data anywhere near fast enough to be useful. I wound up buying a mobil nano router and using that as an access point instead.
