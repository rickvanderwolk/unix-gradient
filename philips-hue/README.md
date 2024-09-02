# Unix gradient Philips Hue

- [Hardware](#hardware)
- [Getting started](#getting-started)
- [Run script](#run-script)

<a id="hardware"></a>
## Hardware

- Raspberry Pi; I currently use a Pi 5 (4GB) but any Pi will probably do just fine
- Philips Hue bridge
- Two full colors Philips Hue lights (for example: two Philips Hue white & color bulbs or two Philips Hue play bars)

<a id="getting-started"></a>
## Getting started

## Install

1. Install Raspberry Pi OS on a SD card. You can easily choose the right image and setup a username / password, Wi-Fi and enable SSH with the [Raspberry Pi OS imager](https://www.raspberrypi.com/software/). I've used the latest recommended image `Raspberry Pi OS (64-bit) - Release date 2024-07-04 - A port of Debian Bookworm with the Raspberry Pi Desktop` in the example below, but I recommend just installing the latest recommended version.
2. Boot the Pi (might take a while depending on which Pi you're using)
3. Connect via SSH `ssh <your-pi-username>@<your-pi-ip>`
4. Clone repository `git clone https://github.com/rickvanderwolk/unix-gradient.git`
5. Run install script `bash unix-gradient/philips-hue/install.sh` (might take a while)
6. [Run script](#run-script)

### Start script on boot (optional)

1. `crontab -e`
2. Choose nano by pressing `1` + `enter`
3. Add to following line `@reboot /home/<your-pi-username>/unix-gradient-philips-hue/bin/python /home/<your-pi-username>/unix-gradient/philips-hue/main.py >> /home/<your-pi-username>/unix-gradient/philips-hue/cronjob.log 2>&1`
4. Press `ctrl` + `x` and then `y` to save
5. Reboot `sudo reboot`

<a id="#run-script"></a>
## Run script

Run script `/home/<your-pi-username>/unix-gradient-philips-hue/bin/python /home/<your-pi-username>/unix-gradient/philips-hue/main.py`.

By default, the script uses the first two full-color lights it finds. Use the `--lights` parameter to specify which lights to use.`/home/<your-pi-username>/unix-gradient-philips-hue/bin/python /home/<your-pi-username>/unix-gradient/philips-hue/main.py --lights <your-light-id-1> <your-light-id-2>`. You can find the light ids by using the API or by running the script without this parameter to see a list of available lights.
