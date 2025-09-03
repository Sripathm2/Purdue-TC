"""pypopper: a file-based pop3 server https://code.activestate.com/recipes/534131-pypopper-python-pop3-server/

Usage:
    python pypopper.py <port> <path_to_message_file>
"""
import logging
import os
import socket
import sys
import traceback
import time

logging.basicConfig(format="%(name)s %(levelname)s - %(message)s")
log = logging.getLogger("pypopper")
log.setLevel(logging.INFO)

class ChatterboxConnection(object):
    END = "\r\n"
    def __init__(self, conn):
        self.conn = conn
    def __getattr__(self, name):
        return getattr(self.conn, name)
    def sendall(self, data, END=END):
        # if len(data) < 50:
        #     log.debug("send: %r", data)
        # else:
        #     log.debug("send: %r...", data[:50])
        data += END
        self.conn.sendall(data.encode())
    def recvall(self, END=END):
        data = []
        while True:
            chunk = self.conn.recv(4096)
            print(chunk)
            return chunk[:-2]


class Message(object):
    def __init__(self, filename):
        msg = open(filename, "r")
        try:
            self.data = data = msg.read()
            self.size = len(data)
        finally:
            msg.close()

def handleRetr(data, msg):
    # log.info("message sent")
    return "+OK %i octets\r\n%s\r\n." % (msg.size, msg.data)

dispatch = dict(
    RETR=handleRetr
)

def serve(host, port, filename):
    assert os.path.exists(filename)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    try:
        if host:
            hostname = host
        else:
            hostname = "localhost"
        log.info("pypopper POP3 serving '%s' on %s:%s", filename, hostname, port)
        while True:
            sock.listen(1)
            conn, addr = sock.accept()
            log.debug('Connected by %s', addr)
            try:
                msg = Message(filename)
                conn = ChatterboxConnection(conn)
                conn.sendall("+OK pypopper file-based pop3 server ready")
                data = conn.recvall().decode('UTF-8')
                print(data)
                number_of_emails = 300 # int(data.split(':')[0])
                for i in range(number_of_emails):
                    try:
                        cmd = dispatch['RETR']
                    except KeyError:
                        conn.sendall("-ERR unknown command")
                    else:
                        conn.sendall(cmd(data, msg))
                    print('number of emails left: ', (number_of_emails - i ))
            finally:
                conn.close()
                msg = None
    except (SystemExit, KeyboardInterrupt):
        log.info("pypopper stopped")
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: [<host>:]<port> <path_to_message_file>")
    else:
        _, port, filename = sys.argv
        if ":" in port:
            host = port[:port.index(":")]
            port = port[port.index(":") + 1:]
        else:
            host = ""
        try:
            port = int(port)
        except:
            print("Unknown port:", port)
        else:
            if os.path.exists(filename):
                serve(host, port, filename)
            else:
                print("File not found:", filename)