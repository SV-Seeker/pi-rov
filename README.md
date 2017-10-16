
# PI-rov

A reaspberry pi powered control platform for controlling an ROV.

## TODO:
- [x] turn off the raspberry pi 3's wifi. ROV uses ethernet for communications.
- [ ] instructions on how to clone / install project
- [ ] script that does all the things automatically
- [ ] script to build an r-pi image
- [ ] setting up a supervisor to keep control scripts running
- [ ] Control loop
    switches and pwm framework for sending commands via WS and receiving it and processing
- [ ] esc control loop
    data from sensor gets processed and turned into ESC output signals for thrusters.
- [ ] one-line/install script for installing on existing rpi installs.
system status message with current output settings for all devices. ( provides feedback to the interface, switch status, thruster output )

## setup
Burn

The default image has ssh disabled by default, to get around that drop a `ssh` file into the boot directory.
The file doesn't have to have an extension or contents.

on OSX:
```shell
cd /Volumes/boot/
touch ssh
```

Eject the card and put it in the pi.
```shell
sudo raspi-config --expand-rootfs
sudo raspi-config nonint do_update
sudo reboot
# re-login
sudo apt-get install -y rpi-update
sudo rpi-update
sudo reboot
# re-login
sudo apt-get install -y git make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
# this disables wifi on next reboot.  Make sure your on ethernet before running this.
echo "\ndtoverlay=pi3-disable-wifi" >> /boot/config.txt
```

Add this to the bottom of your `.bashrc` file
```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

<!-- TODO: clone down ROV project -->
```shell
cd rov
pyenv install
```


# local development setup

```
pyenv virtualenv rov
pyenv activate
```
