#!/usr/bin/env bash
ip route add 172.17.0.0/24 via 10.0.0.0 dev server5-eth0
python3 /work/Python/VideoConferencing/webcam.py -v --host 10.0.1.9 --play-from /video_conferencing/people.mp4