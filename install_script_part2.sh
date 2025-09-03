#!/bin/bash

# Update the apt package index
sudo apt-get update
echo "apt package index updated"

# installing python pip requirements
pip3 install -r requirements.txt

# creating FTP files/ Web Files and Video streaming files
cd PrepFiles
python Setup_FTP.py
./Setup_Web.sh ./top_500_urls.txt
./Setup_Video_Streaming.sh

cd ../Controlled_dataset_collection
make pull-containernet-docker-image
echo "pull-containernet-docker-image complete"
make build-dpdk-host-docker-image
echo "build-dpdk-host-docker-image complete"
make super-clean

mkdir -p ../data/collected_dataset
cp ../PrepFiles/top_500_urls.txt ../data/web/

# modprobe br_netfilter
# docker info | grep "Network driver"
# echo "modprobe br_netfilter complete"
