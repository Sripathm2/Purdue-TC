from scapy.all import *
from configparser import ConfigParser
import os

config = ConfigParser()
config.read('/work/config.ini')
web_config = config["WEB"]


if __name__ == "__main__":
    print('starting http server')
    os.system('nginx -c ' + web_config['nginx_conf_file'])
    

    