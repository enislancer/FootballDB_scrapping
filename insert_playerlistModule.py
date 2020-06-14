import requests
from bs4 import BeautifulSoup
import argparse
import mysql.connector
import certifi
import urllib3



################################################################
# This is the sample instructions to insert the player info into playerlist.
# python3 insert_playerlistModule.py -season 2014-2015 -league esp-primera-division -page 1

# direct write the info for inserting..... for saving time.
#################################################################

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Password@302",
  database="soccer"
)
mycursor = mydb.cursor()

def switch_season(argument):
    switcher = {
      "2014-2015": 1,
      "2015-2016": 2,
      "2016-2017": 3,
      "2017-2018": 4,
      "2018-2019": 5,
    }
    return switcher.get(argument, "null")
def switch_league(argument):
    switcher = {
        "srb-super-liga": 15    #Serbia
    }
    return switcher.get(argument, "null")

def insert_playerList(season=None , league=None, page = None):

    pageNumber = page
    print(f"-------------------------------{season}-{pageNumber}page start-----------------------------------------")
    if season:
        URL = f"https://www.worldfootball.net/players_list/{league}-{season}/nach-mannschaft/{page}/"
    else:
        #URL = f"https://www.worldfootball.net/players_list/esp-primera-division-2014-2015/nach-mannschaft/1/"
        print("Enter the season !")
        return

    page = requests.get(URL , headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find('table', class_="standard_tabelle")
    tr_results = results.find_all("tr")
    #player_info_list = []
    i = 0
    for tr in tr_results:
        all_td = tr.find_all("td")
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        if(len(all_td)) :
            player_name = all_td[0].text
            player_born = all_td[3].text
            player_height = all_td[4].text
            player_position = all_td[5].text
            href_info = all_td[0].find("a")['href']

            url = "https://www.worldfootball.net"+href_info
            player_adding_info = get_more_player_info(url , player_name)
            #per_player_info = [player_name, player_born,player_adding_info[1],player_adding_info[0], \
            #                   player_height, player_adding_info[2] \
            #                   ,player_adding_info[3], player_position]
            """print(player_name, player_born,player_adding_info[1],player_adding_info[0], \
                               player_height, player_adding_info[2] \
                              ,player_adding_info[3], player_position)
            player_name = per_player_info[0]
            player_birthday = per_player_info[1]
            player_nation = per_player_info[2]"""

            sql = f'SELECT * FROM playerlist WHERE player_name ="{player_name}" and birthday = "{player_born}" and nationality like "%{player_adding_info[1]}%"'
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            if len(myresult):
                print(f"There is already in playerlist - {player_name} : {player_born}")
            else:
                print(f"this is new - {player_name} : {player_born}")
                sql = "INSERT INTO playerlist (player_name, birthday , nationality, img_src, height, weight, foot" \
                      ", position ) VALUES (%s, %s , %s, %s, %s, %s, %s, %s)"
                val = (player_name, player_born,player_adding_info[1],player_adding_info[0], \
                               player_height, player_adding_info[2] \
                               ,player_adding_info[3], player_position)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")

            print(f"--------{i+1}th---------------")
            #player_info_list.append(per_player_info)
            i +=1

    print(f"-------------------------------{season}-{pageNumber}page end----------------------------------------------------")
    #return player_info_list

def get_more_player_info(url , player_name):

    page = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find('div', itemtype="http://schema.org/Person")
    player_img = results.find("img", alt = player_name)["src"]

    player_nation_container = results.find(string = "Nationality:").findNext("td")
    player_nation_container = player_nation_container.find_all("img")
    count = 0;
    player_nation=""
    for i in player_nation_container:
        if count > 0:
            player_nation +=","
        player_nation += i['alt']
        count += 1

    player_weight = "???"
    if results.find(string="Weight:"):
        player_weight = results.find(string="Weight:").findNext("td").text.strip()
    player_foot = "???"
    if results.find(string="Foot:"):
        player_foot = results.find(string = "Foot:").findNext("td").text.strip()

    return_list = [player_img, player_nation, player_weight, player_foot]
    return return_list

"""for x in range(1, 12):
    insert_playerList("2014-2015", "srb-super-liga",x)
print("-----------------2014-2015 end----------------------------")
for x in range(1, 11):
    insert_playerList("2015-2016", "srb-super-liga",x)
print("-----------------2015-2016 end----------------------------")
for x in range(1, 11):
    insert_playerList("2016-2017", "srb-super-liga",x)
print("-----------------2016-2017 end----------------------------")"""
for x in range(1, 11):
    insert_playerList("2017-2018", "srb-super-liga",x)
print("-----------------2017-2018 end----------------------------")
for x in range(1, 11):
    insert_playerList("2018-2019", "srb-super-liga",x)
print("-----------------2018-2019 end----------------------------")

















