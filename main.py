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
from nordvpn_switcher import initialize_VPN,rotate_VPN



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
        options.add_argument("--disable-javascript")
        options.add_argument("--disable-plugins-discovery");
        options.add_argument("--start-maximized")
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--incognito")
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

    def roboCheck(self):
        robo_xp = '//*[contains(text(),"Additional security check is required")]'
        robo_check_element = self.driver.find_elements(By.XPATH, robo_xp)

        if len(robo_check_element) >0:
            input("Please SOLVE PUZZLE to continue")

        if "Incapsula incident ID" in self.driver.page_source:
            self.driver.delete_all_cookies()
            self.driver.get(self.link)
            time.sleep(2)
            self.driver.delete_all_cookies()
            self.driver.get(self.link)
            time.sleep(2)

        if "Incapsula incident ID" in self.driver.page_source:
            rotate_VPN()
            time.sleep(2)
            self.driver.delete_all_cookies()
            self.driver.get(self.link)
            time.sleep(3)
            self.roboCheckBoolian=True

        else:
            self.roboCheckBoolian = False




    def generate_initial_links(self):
        self.driver.get("https://www.menards.com/main/sitemap.html")
        
        input("Enter to continue")
        elements = self.driver.find_elements(By.XPATH, '//*[@class="card-body pt-0 pl-0"]//div/a')
        links = [i.get_attribute("href") for i in elements]
        names = [i.get_attribute("text") for i in elements]

        df = pd.DataFrame([names,links]).T
        df.columns = ['cat','link']
        df.to_csv("initial_links.csv",index=None)

    def iterate(self):
        with open("lastcat.txt","r") as fl3:
            l = fl3.read()
            
        df1 = pd.read_csv("initial_links.csv")
        ind = df1[df1.link == l].index
        df1 = df1.iloc[ind[0]+1:]



        for link in df1.link:
            self.link = link
            if not link in self.used_links:
                self.used_links.append(link)
                self.driver.get(link)

                while True:
                    self.roboCheck()
                    if self.roboCheckBoolian == False:
                        break
                
                time.sleep(random.choice([10,15]))
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.choice([12,16]))
                xp = '//*[@width="500"]//ancestor::*[@class="row"]//ancestor::a'
                elements = self.driver.find_elements(By.XPATH,xp)

                if len(elements) ==0:
                    with open("2failed.json", "a") as fl:
                        fl.write(link+ "\n")
                        fl.close()
                else:
                    for ele in elements:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)
                        time.sleep(3)
                    
                    elements = self.driver.find_elements(By.XPATH,xp)
                    trees = [etree.HTML(i.get_attribute("outerHTML")) for i in elements]
                    name_link = [{link:[tree.xpath('//img/following-sibling::*//text()'),tree.xpath('//@href')]} for tree in trees]
                    
                    for i in name_link:
                        self.master_list.append(i)
                    with open("2nd.json", "a") as fl:
                        json.dump(self.master_list,fl)
                        fl.write("\n")
                        fl.close()
                    self.master_list = []
                    with open("lastcat.txt","w") as fl2:
                        fl2.write(link)
                        fl2.close()
                    self.driver.delete_all_cookies()
            else:
                pass





if __name__ == "__main__":
    scraper = Scraper()
    scraper.iterate()

#103



#product details
#//*[@id="searchItems"]//*[@class="search-item"]//*[@class="text-dark"]

#approach1
#//*[@class="row"][2]//*[@width="500"]

#approach2
#open all links in all rows
#it will open duplicates but will be able to fetch required details
#make sure link is of menards

#//*[@class="w-100 p-2 col-xl-2 col-md-4 col-6 col-lg-3  d-block d-sm-block d-md-block d-lg-block d-xl-block"]|//*[@class="w-100 p-2 col-xl-2 col-md-4 col-6 col-lg-3 offset-xl-0 offset-lg-3 d-block d-sm-block d-md-block d-lg-block d-xl-block"]|//*[@class="w-100 p-2 col-md-4 col-6 col-lg-3  d-block d-sm-block d-md-block d-lg-block d-xl-block"]|//*[class="w-100 p-2 col-md-3 col-6  d-block d-sm-block d-md-block d-lg-block d-xl-block"]

#layer2
#//*[@class="position-relative dynamic-image"]