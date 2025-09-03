from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from configparser import ConfigParser
import os
import sys
import random
import time
import numpy as np

config = ConfigParser()
config.read('/work/config.ini')
web_config = config["WEB"]


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


if __name__ == "__main__":
    # sleep_time = 25

    number_of_websites = int(sys.argv[1])

    url_list_file = f = open(web_config['list_of_urls_file'], "r")
    url_list = url_list_file.readlines()
    url_list = [item[:-1] for item in url_list]

    a = 1.1
    zipf_dist = np.random.default_rng().zipf(a, size=number_of_websites)
    zipf_dist = (zipf_dist/float(max(zipf_dist)))*(len(url_list)-1)

    url_list = [url_list[int(i)] for i in zipf_dist]

    min_wait = 5
    max_wait = 52 if number_of_websites < 5 else 10
    sleep_time = np.random.uniform(min_wait, max_wait, number_of_websites)


    for index, url in enumerate(url_list):
        # time.sleep(float(sleep_time[index]))
        time.sleep(sleep_time[index])
        try:
            # Use the browser Navigation Timing API to get some numbers:
            # https://developer.mozilla.org/en-US/docs/Web/API/Navigation_timing_API
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            driver = webdriver.Firefox(options=opts)
            driver.set_page_load_timeout(30)

            driver.get('http://10.0.1.8:8888/' + url.replace('https://', ''))
            navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
            dom_complete = driver.execute_script("return window.performance.timing.domComplete")
        except:
            pass

    os.system('rm -rf rm /work/geckodriver.log')
