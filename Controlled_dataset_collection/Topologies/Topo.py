#!/usr/bin/python
import os
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from configparser import ConfigParser, ExtendedInterpolation

setLogLevel('info')

config = ConfigParser(interpolation=ExtendedInterpolation())
config.read('/work/config.ini')
topo_config = config['TOPOLOGY']

code_vol = topo_config['code_vol']
ftp_vol = topo_config['ftp_vol']
web_vol = topo_config['web_vol']
video_streaming_vol = topo_config['video_streaming_vol']
video_conferencing_vol = topo_config['video_conferencing_vol']
volumes = [code_vol, ftp_vol, web_vol, video_streaming_vol, video_conferencing_vol]

net = Containernet(controller=Controller)

info('*** Adding controller\n')
net.addController('c0')

info('*** Adding docker containers\n')
client1 = net.addDocker('client1', ip=topo_config['client1'], dimage=topo_config['docker_image'], volumes=volumes)
client2 = net.addDocker('client2', ip=topo_config['client2'], dimage=topo_config['docker_image'], volumes=volumes)
client3 = net.addDocker('client3', ip=topo_config['client3'], dimage=topo_config['docker_image'], volumes=volumes)
client4 = net.addDocker('client4', ip=topo_config['client4'], dimage=topo_config['docker_image'], volumes=volumes)
server1 = net.addDocker('server1', ip=topo_config['server1'], dimage=topo_config['docker_image'], volumes=volumes)
server2 = net.addDocker('server2', ip=topo_config['server2'], dimage=topo_config['docker_image'], volumes=volumes)
server3 = net.addDocker('server3', ip=topo_config['server3'], dimage=topo_config['docker_image'], volumes=volumes)
server4 = net.addDocker('server4', ip=topo_config['server4'], dimage=topo_config['docker_image'], volumes=volumes)
server5 = net.addDocker('server5', ip=topo_config['server5'], dimage=topo_config['docker_image'], volumes=volumes)

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')

info('*** Creating links\n')
net.addLink(client1, s1)
net.addLink(client2, s1)
net.addLink(client3, s1)
net.addLink(client4, s1)
net.addLink(server1, s2)
net.addLink(server2, s2)
net.addLink(server3, s2)
net.addLink(server4, s2)
net.addLink(server5, s2)
net.addLink(s1, s2, cls=TCLink, delay=topo_config['link_delay'], bw=int(topo_config['link_bw']))


client1.cmd('ifconfig client1-eth0 mtu 1500 up')
client2.cmd('ifconfig client2-eth0 mtu 1500 up')
client3.cmd('ifconfig client3-eth0 mtu 1500 up')
client4.cmd('ifconfig client4-eth0 mtu 1500 up')
server1.cmd('ifconfig server1-eth0 mtu 1500 up')
server2.cmd('ifconfig server2-eth0 mtu 1500 up')
server3.cmd('ifconfig server3-eth0 mtu 1500 up')
server4.cmd('ifconfig server4-eth0 mtu 1500 up')
server5.cmd('ifconfig server5-eth0 mtu 1500 up')


client1.cmd("ethtool -K client1-eth0 tx off sg off tso off")
client2.cmd("ethtool -K client2-eth0 tx off sg off tso off")
client3.cmd("ethtool -K client3-eth0 tx off sg off tso off")
client4.cmd("ethtool -K client4-eth0 tx off sg off tso off")
server1.cmd("ethtool -K server1-eth0 tx off sg off tso off")
server2.cmd("ethtool -K server2-eth0 tx off sg off tso off")
server3.cmd("ethtool -K server3-eth0 tx off sg off tso off")
server4.cmd("ethtool -K server4-eth0 tx off sg off tso off")
server5.cmd("ethtool -K server5-eth0 tx off sg off tso off")


info('*** Starting network\n')
net.start()

info('*** Testing connectivity\n')
net.ping()

info('*** setting up tcpdump\n')
os.system('apt update')
os.system('apt install -y tcpdump')
os.system('ethtool -K s1-eth5 tx off sg off tso off')
os.system('ethtool -K s1-eth5 gso off')
os.system('ethtool -K s1-eth5 flo off')

info('*** Running CLI\n')
CLI(net)
