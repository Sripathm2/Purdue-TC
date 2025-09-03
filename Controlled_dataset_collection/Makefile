#### Start of Makefile ####

########################################################################
#### a. Setting up and debugging workspace commands
########################################################################


######## a.1 Setting up repositories and downlaoding docker images ########

git-submodules:
	git submodule update --init --recursive

pull-containernet-docker-image:
	docker pull containernet/containernet

build-dpdk-host-docker-image:
	sudo docker build --no-cache --tag=dpdk_host -f Docker/Dockerfile.dpdk_host Docker/


######## a.2 cleaning up ########

clean:
	-docker stop $$(docker ps -a -q --filter="name=mn.*")
	-docker remove $$(docker ps -a -q --filter="name=mn.*")
	-docker stop containernet
	-docker remove containernet
	-sudo rm -rf config.ini config.ini.bak temp ./log run.py *.txt1 w*

super-clean:clean
	-sudo rm -rf *.pcap *.capture *.png *.log

########################################################################
#### b. Running topologies commands
########################################################################

#### b.1 setup the config
setup-controlled-config:
	cp ./Configurations/controlled_config.ini ./config.ini

setup-congestion-control-algorithm:
	sudo sysctl -w net.core.default_qdisc=fq_codel
	sudo sysctl -w net.ipv4.tcp_congestion_control=$(cc_alg)
	sudo sysctl --system
	sysctl net.ipv4.tcp_congestion_control

setup-bbr-congestion-control-algorithm:
	sudo sysctl -w net.core.default_qdisc=fq
	sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
	sudo sysctl --system
	sysctl net.ipv4.tcp_congestion_control

#### b.2 Setup the topology.
setup-topology:
	docker run --name containernet -it --rm --privileged --expose 3000 --pid='host' -v /var/run/docker.sock:/var/run/docker.sock -v ./:/work/ containernet/containernet python3 /work/Topologies/Topo.py

#### b.3 capturing traffic

start-client-pcap-capture:
	docker exec -it mn.$(host_name) tcpdump -i $(host_name)-eth0 -w /work/$(host_name).pcap

start-client-pcap-capture-as-text:
	docker exec -it mn.$(host_name) tcpdump -i $(host_name)-eth0 > ./$(host_name).capture

start-switch-pcap-capture:
	docker exec -it containernet tcpdump --immediate-mode -i $(intf_name) -w /work/$(capture_name).pcap

start-switch-pcap-capture-as-text:
	docker exec -it containernet tcpdump -i $(intf_name) > ./$(intf_name).capture

#### b.4 live topology
live-topo: setup-controlled-config setup-topology

########################################################################
#### d. Simulating different applications
########################################################################
# choose and run one of the b.x before running these.

#### d.0 iperf based commands
start-iperf-server:
	docker exec -it mn.server1 iperf -s -u

start-iperf-client:
	docker exec -it mn.client1 /work/Bash/iperf.sh


#### d.1 FTP based commands
start-ftp-setup:
	docker exec -it mn.server3 python3 /work/Python/FTP/setup_ftp_files.py

start-ftp-server:
	docker exec -it mn.server3 python3 /work/Python/FTP/ftp_server.py

start-ftp-client:
	docker exec -it $(ftp_client) python3 /work/Python/FTP/ftp_client.py $(num_files)

#### d.2 Web based commands
start-web-server:
	docker exec -it mn.server4 python3 /work/Python/Web/web_get_webpage_for_nginx.py

start-web-client:
	docker exec -it $(web_client) python3 /work/Python/Web/web_get_webpage_to_pcap_selenium.py $(num_websites)

#### d.3 Email based commands
start-email-server:
	docker exec -it mn.server1 python3 /work/Python/Pop3Email/pop3_server.py 10.0.1.5:10111 /work/Python/Pop3Email/message.txt

start-email-client:
	docker exec -it $(email_client) python3 /work/Python/Pop3Email/pop3_client.py $(num_email)

#### d.4 Video streaming based commands
start-video-streaming-server:
	docker exec -it mn.server2 python3 /work/Python/VideoStreaming/Dash_server.py

start-video-streaming-client:
	docker exec -it $(vs_client) python3 /work/Python/VideoStreaming/Dash_client.py $(video_index)

#### d.4 Video conferencing server based commands
start-video-conferencing-server:
	docker exec -it mn.server5 /work/Python/VideoConferencing/webrtc-server.sh

start-video-conferencing-sender:
	docker exec -it mn.server5 /work/Python/VideoConferencing/webrtc-sender.sh

start-video-conferencing-receiver:
	docker exec -it $(vc_client) /work/Python/VideoConferencing/webrtc-reciever.sh $(call_length)

########################################################################
#### e Experiments commands
########################################################################

#### e.1 Controlled pcap collection
run-controlled-pcap-collection:
	cp ./Python/Experiments/controlled_dataset_collection.py ./run.py
	sudo python3 run.py