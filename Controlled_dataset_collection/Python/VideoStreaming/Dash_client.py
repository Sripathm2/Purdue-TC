from configparser import ConfigParser
import os
import sys

config = ConfigParser()
config.read('/work/config.ini')
video_streaming_config = config["VideoStreaming"]

if __name__ == "__main__":
    video_index_to_transfer = int(sys.argv[1])

    files = video_streaming_config['mpd_file_location'].split(':')
    mpd_urls = video_streaming_config['mpd_url'].split('::')

    file = files[video_index_to_transfer]
    mpd_url = mpd_urls[video_index_to_transfer]

    print('Starting script')
    os.system('python3 ' + video_streaming_config['dash_client_qoe_file'] + ' -m ' + mpd_url + ' -p netflix')
