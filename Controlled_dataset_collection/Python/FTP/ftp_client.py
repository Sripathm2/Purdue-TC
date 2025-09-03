import random
from configparser import ConfigParser
import os
import sys

config = ConfigParser()
config.read('/work/config.ini')
ftp_config = config["FTP"]

if __name__ == "__main__":

    files_to_ftp = []
    number_of_files = int(sys.argv[1])

    for path, subdirs, files in os.walk(ftp_config['files_directory']):
        for name in files:
            file_name = os.path.join(path, name)
            file_name = file_name.replace(ftp_config['files_directory'], '')
            files_to_ftp.append(file_name)

    random.shuffle(files_to_ftp)

    if number_of_files >= len(files_to_ftp):
        number_of_files = len(files_to_ftp)

    for i in range(number_of_files):
        file = files_to_ftp[i]
        os.system('wget ftp://' + ftp_config['username'] + ':' + ftp_config['password'] + '@' + '10.0.1.7' + '/' +file)
        os.system('rm -rf /work/'+file)