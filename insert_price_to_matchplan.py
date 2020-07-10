import requests
from bs4 import BeautifulSoup
import argparse
import mysql.connector
import certifi
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys

http = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="soccer"
)

mycursor = mydb.cursor()
def switch_season(argument):
    switcher = {
      "2010-2011": 19,
      "2011-2012": 17,
      "2012-2013": 15,
      "2013-2014": 13,
      "2014": 6,
      "2013": 14,
      "2012": 16,
      "2011": 18, 
      "2010": 20, 
    }
    return switcher.get(argument, "null")
def switch_league(argument):
    switcher = {
      "esp-primera-division": 16,  #spain
      "eng-premier-league": 6,   #England
      "bundesliga": 8,   #Germany
      "ita-serie-a" : 11,  #italy
      "fra-ligue-1" : 7,   #france
      "ned-eredivisie": 12,  #Netherland
      "aut-bundesliga": 1,  #Austria
        "por-primeira-liga": 14,  #portugal
        "por-liga-sagres": 14,
        "por-liga-zon-sagres":14,
        "gre-superleague": 9,   #Greece
        "tur-sueperlig": 19,   #Turkey
        "nor-eliteserien": 13,  #Norway
        "nor-tippeligaen":13,
        "swe-allsvenskan": 17,  #Sweden
        "sui-super-league": 18,   #Swiztland
        "den-superliga": 5,     #Denmark
        "den-sas-ligaen":5,
        "ukr-premyer-liga": 20,     #Ukraine
        "bul-a-grupa": 2,       #bulgaria
        "cze-1-fotbalova-liga": 3,      #Chezch
        "cze-gambrinus-liga": 3,
        "cro-1-hnl": 4 ,          #Croatia
        "hun-nb-i": 10,     #Hungary
        "hun-nb1": 10,
        "hun-otp-liga":10,
        "srb-super-liga": 15    #Serbia
    }
    return switcher.get(argument, "null")

chrome_driver_path = 'H:\workstation\Soccer+betting\Soccer_scrapping\chromedriver'
#chrome_options = Options()
#chrome_options.add_argument('--headless')
#webdriver = webdriver.Chrome(
#  executable_path=chrome_driver_path
#)

def insert_price_to_matchplan():
    basic_match_href_url = "https://www.oddsportal.com/soccer/austria/tipico-bundesliga-2018-2019/altach-lask-linz-EFzW1EUn/"
    
    first_two_url = basic_match_href_url + "#1X2;2" 
    OU_url  =  basic_match_href_url + "#over-under;2"
    AH_url = basic_match_href_url + "#ah;2"

    get_1X2data(first_two_url)

    

def get_1X2data(url):

    """options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome( executable_path=chrome_driver_path)
    driver.get(url)
    tfoot = driver.find_elements_by_tag_name('tfoot')
    print(tfoot[0].text)
    driver.quit()"""
    driver = webdriver.Firefox(executable_path = 'H:\workstation\Soccer+betting\Soccer_scrapping\geckodriver')
    # get web page
    driver.get(url)
    # execute script to scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # sleep for 30s
    time.sleep(30)
    # driver.quit()        
        

insert_price_to_matchplan()