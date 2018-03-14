
# PI-rov

A reaspberry pi powered control platform for controlling an ROV.

## TODO:
- [ ] turn off the raspberry pi 3's wifi
- [ ] instructions on how to clone / install project
- [ ] script that does all the things automatically
- [ ] script to build an r-pi image
- [ ] setting up a supervisor to keep control scripts running
- [ ] Control loop
    switches and pwm framework for sending commands via WS and receiving it and processing
- [ ] esc control loop
    data from sensor gets processed and turned into ESC output signals for thrusters.
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
sudo apt-get install -y git make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev supervisor
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
```

Add this to the bottom of the pi users `.bashrc` file
```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

```shell
git clone https://github.com/SV-Seeker/pi-rov.git rov
cd rov
pyenv install
pyenv virtualenv rov-venv
./script/rov/update
```
installing python takes a while.

# local development setup

```
git clone https://github.com/SV-Seeker/pi-rov.git
git remote add rov pi@rov.local:/home/pi/rov/
cd pi-rov
pyenv install
pyenv virtualenv rov
pyenv activate
```

## deploying

```bash
./script/deploy
```
