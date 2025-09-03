#!/bin/bash

while :
do
	iperf -c 10.0.1.5 -u -b 100m -t 1
	sleep 2
done