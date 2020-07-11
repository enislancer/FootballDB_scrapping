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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

options = Options()
options.headless = True
options.add_argument("--ignore-certificate-errors-spki-list");
options.add_argument("--ignore-ssl-errors");
options.add_argument("test-type");
options.add_argument("-incognito");
options.add_argument("no-sandbox");
options.add_argument("--start-maximized");
options.add_argument("--window-size=1920,1200")
chrome_driver_path = 'H:\workstation\Soccer+betting\Soccer_scrapping\chromedriver'



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


def insert_price_to_matchplan():
    basic_match_href_url = "https://www.oddsportal.com/soccer/austria/tipico-bundesliga-2018-2019/admira-st-polten-rZjCogp6/"
    odd_price = []
    first_two_url = basic_match_href_url + "#1X2;2" 
    OU_url  =  basic_match_href_url + "#over-under;2"
    AH_url = basic_match_href_url + "#ah;2"
    print("--------- start scraping 1X2 data --------------------")
    WD_value = get_1X2data(first_two_url)
    if len(WD_value) == 3:
      odd_price.append(WD_value)
    else:
      print("  Average counts is smaller than 3")
      return
    print("--------- start scraping Over Under data --------------------")
    odd_price.append(get_Over_Underdata(OU_url))
    print("--------- start scraping Asian Handicap data --------------------")
    odd_price.append(get_AH_Data(AH_url))
    print("--------- End scraping  data --------------------")
    print(odd_price)
    

def get_1X2data(url):
    return_val = []
  
    driver = webdriver.Chrome( options = options,  executable_path=chrome_driver_path)
    driver.get(url)
   
    tfoot = driver.find_elements_by_tag_name('tfoot')
    aver_element = tfoot[0].find_element_by_class_name("aver")
    if aver_element:
       av_values = aver_element.find_elements_by_class_name("right")
       if len(av_values) > 2:
          return_val.append(av_values[0].text)
          return_val.append(av_values[1].text)
          return_val.append(av_values[2].text)
       else:
         print("  Average counts is smaller than 3")
    else: 
       print(" Not Found aver elements")
    driver.quit()
    
    return return_val  


def get_Over_Underdata(url):
    return_val = ['','','','']
    driver = webdriver.Chrome( options = options,  executable_path=chrome_driver_path)
    driver.get(url)
    root_data = driver.find_element_by_id("odds-data-table")
    
    containers = root_data.find_elements_by_class_name('table-container')
    for container in containers:
      #print(container.text)
      strong_element = container.find_elements_by_tag_name('strong')
      if len(strong_element):
        if strong_element[0].text == "Over/Under +2.5":
          #tr = strong_element[0]
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            
            #print(f"---{span_elements[0].text}------")
            return_val[1] = span_elements[0].text
            return_val[0] = span_elements[1].text

        if strong_element[0].text == "Over/Under +3.5":
          #tr = strong_element[0]
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[3] = span_elements[0].text
            return_val[2] = span_elements[1].text
      
    print(return_val)
    driver.quit()
    return return_val

def get_AH_Data(url):
    return_val = ['','','','','','','','','','','','','','','','','','','','']
    driver = webdriver.Chrome( options = options,  executable_path=chrome_driver_path)
    driver.get(url)
    root_data = driver.find_element_by_id("odds-data-table")
    containers = root_data.find_elements_by_class_name('table-container')
    for container in containers:
      
      strong_element = container.find_elements_by_tag_name('strong')
      if len(strong_element):
        if strong_element[0].text == "Asian handicap -3.5":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[1] = span_elements[0].text
            return_val[0] = span_elements[1].text
        if strong_element[0].text == "Asian handicap -3":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[3] = span_elements[0].text
            return_val[2] = span_elements[1].text
        if strong_element[0].text == "Asian handicap -2.5":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[5] = span_elements[0].text
            return_val[4] = span_elements[1].text
        if strong_element[0].text == "Asian handicap -2":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[7] = span_elements[0].text
            return_val[6] = span_elements[1].text
        if strong_element[0].text == "Asian handicap -1.5":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[9] = span_elements[0].text
            return_val[8] = span_elements[1].text
        if strong_element[0].text == "Asian handicap -1.25":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[11] = span_elements[0].text
            return_val[10] = span_elements[1].text
        if strong_element[0].text == "Asian handicap -1":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[13] = span_elements[0].text
            return_val[12] = span_elements[1].text
        if strong_element[0].text == "Asian handicap -0.5":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[15] = span_elements[0].text
            return_val[14] = span_elements[1].text
        if strong_element[0].text == "Asian handicap -0.25":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[17] = span_elements[0].text
            return_val[16] = span_elements[1].text
        if strong_element[0].text == "Asian handicap 0":
          span_elements = container.find_elements_by_class_name('nowrp')
          if len(span_elements):
            return_val[19] = span_elements[0].text
            return_val[18] = span_elements[1].text
    
    driver.quit()
    print(return_val)
    return return_val

insert_price_to_matchplan()