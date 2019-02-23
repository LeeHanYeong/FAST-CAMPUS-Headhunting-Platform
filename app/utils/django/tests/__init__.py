import subprocess

from selenium import webdriver


def get_chromedriver():
    process = subprocess.Popen('which chromedriver', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    o, e = process.communicate()
    chrome_driver = o.decode('utf-8').strip()
    return webdriver.Chrome(chrome_driver)
