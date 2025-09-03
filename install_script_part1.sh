#!/bin/bash
# Update the apt package index
sudo apt-get update
echo "apt package index updated"


# Install packages to allow apt to use a repository over HTTPS
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    ffmpeg python3.10 unzip tcpdump openvswitch-switch openvswitch-common python3-pip
    
echo "packages to allow apt to use a repository over HTTPS installed"

# Add Docker's official GPG key:
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
echo "apt package index updated again"


# Install the latest version of Docker Engine and containerd
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
echo "Docker Engine and containerd installed"

# Verify that Docker Engine is installed correctly by running the hello-world image
sudo docker run hello-world
echo "hello-world image run"
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
echo "user added to docker group"