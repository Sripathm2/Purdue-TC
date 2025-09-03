from configparser import ConfigParser
import os

config = ConfigParser()
config.read('/work/config.ini')
video_streaming_config = config["VideoStreaming"]

if __name__ == "__main__":

    if video_streaming_config['get_files'] == 'True':
        print('starting retrieval of video file and processing them into chunks')
        os.system(
            video_streaming_config['getting_videos_and_processsing'] + ' ' + video_streaming_config['video_files'])
        print('done')

    print('starting http server')
    os.system('nginx -c ' + video_streaming_config['nginx_conf_file'])
