#!/bin/sh

# Install fonts used for image generation
echo "deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty multiverse
deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-updates multiverse
deb http://us-west-2.ec2.archive.ubuntu.com/ubuntu/ trusty-backports main restricted universe multiverse" | sudo tee /etc/apt/sources.list.d/multiverse.list
echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections
sudo apt-get update
sudo apt install ttf-mscorefonts-installer -y
sudo fc-cache -f

# Install dependencies
poetry install

# Install pre-commit hook
poetry run pre-commit install
