from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import json
import pandas as pd
import os
from lxml import etree
import random
from selenium_stealth import stealth

class Scraper():
    #Initialising Scraper
    def __init__(self):
        self.robot = '//*[contains(text(),"To proceed, please verify that you are not a robot.")]'
        self.master_dict = {'cat':[],'link':[]}
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-plugins-discovery");
        options.add_argument("--start-maximized")
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(executable_path="./chromedriver",options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        stealth(self.driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

        self.used_links = []
        self.master_list = []
        self.refresh_counter = 0
        self.roboCheckBoolian=True

    def open1(self):

        self.driver.get("https://www.overstock.com/Home-Garden/Sofas-Couches/2027/subcat.html")
        xp = '//*[@class="department__imgBox--FJOfI0"]//a[1]'
        ele = self.driver.find_elements(By.XPATH,xp)
        ele = [i.get_attribute('href') for i in ele]
        print(ele)
        for i in ele:
            self.driver.get(i)

    def open2(self):
        self.driver.get("https://www.overstock.com/Home-Garden/Sofas-Couches/2027/subcat.html")
        xp = '//*[@id="sn-wrapper"]/main/div/div[2]/div/section/div[2]/nav/ul/li/a'
        ele = self.driver.find_elements(By.XPATH,xp)
        ele = [i.get_attribute('href') for i in ele]
        print(ele)
        for i in ele:
            self.driver.get(i)

Scraper().open2()