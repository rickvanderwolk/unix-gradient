# Unix gradient Philips Hue

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
3. Add to following line `@reboot /home/pimonitorstudio/unix-gradient/philips-hue/main.py >> /home/<your-pi-username>/unix-gradient/philips-hue/cronjob.log 2>&1`
4. Press `ctrl` + `x` and then `y` to save
5. Reboot `sudo reboot`

<a id="#run-script"></a>
## Run script

Run script `/home/pimonitorstudio/unix-gradient-philips-hue/bin/python /home/pimonitorstudio/unix-gradient/philips-hue/main.py`. You probably need to use `sudo` to run the script as we use the GPIO pins for communication with the LED strip.

