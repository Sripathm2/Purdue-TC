#!/usr/bin/env python

# Copyright (C) 2007 Giampaolo Rodola' <g.rodola@gmail.com>.
# Use of this source code is governed by MIT license that can be
# found in the LICENSE file.
# modified over.

"""A basic FTP server which uses a DummyAuthorizer for managing 'virtual
users', setting a limit for incoming connections and a range of passive
ports.
"""

import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from configparser import ConfigParser

config = ConfigParser()
config.read('/work/config.ini')
ftp_config = config["FTP"]



def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user(ftp_config['username'], ftp_config['password'], ftp_config['files_directory'], perm='elradfmwMT')
    authorizer.add_anonymous(ftp_config['files_directory'])

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    # handler.masquerade_address = '151.25.42.11'
    handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 21)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 10
    server.max_cons_per_ip = 100

    # start ftp server
    server.serve_forever()


if __name__ == '__main__':
    main()