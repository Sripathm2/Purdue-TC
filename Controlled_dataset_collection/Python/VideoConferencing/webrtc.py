import time
import os
import argparse
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        __doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--call_duration', '-c', type=int)
    args = parser.parse_args()
    url = 'http://10.0.1.9:8080/'
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless=new")

    chrome_service = Service(log_path=os.path.devnull)
    driver = Chrome(options=chrome_options, service=chrome_service)
    driver.get(url)
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="use-stun"]').click()
    driver.find_element(By.XPATH, '//*[@id="start"]').click()
    time.sleep(args.call_duration+10)
    driver.find_element(By.XPATH, '//*[@id="stop"]').click()
    driver.close()


