import requests
from bs4 import BeautifulSoup
import argparse
import mysql.connector

import certifi
import urllib3

http = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

################################################################
# This is the sample instructions to insert the team info(team_list and season_league_team into) into database.
# python3 Get_season_league_teamname.py -season 2014-2015 -league esp-primera-division
#################################################################

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="soccer"
)
mycursor = mydb.cursor()
def switch_season(argument):
    switcher = {
      "2014-2015": 1,
      "2015-2016": 2,
      "2016-2017_2" : 3,
      "2016-2017": 3,
      "2017-2018": 4,
      "2018-2019": 5,
        "2014": 6,
        "2015": 7,
        "2016": 8,
        "2017": 9,
        "2018": 10,
        "2019": 11,
    }
    return switcher.get(argument, "null")
def switch_league(argument):
    switcher = {
        "esp-primera-division": 16 , #spain
        "srb-super-liga": 15    #Serbia
    }
    return switcher.get(argument, "null")
def insert_player_wholecareer(season=None , league=None, pageNumber = None):

    ################################### page url check start ###############################
    print(f"-------------------------------{season}-{pageNumber}page start-----------------------------------------")
    URL = f"https://www.worldfootball.net/players_list/{league}-{season}/nach-mannschaft/{pageNumber}/"
    page = requests.get(URL , headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find('table', class_="standard_tabelle")
    tr_results = results.find_all("tr")

    i = 1
    for tr in tr_results:
        all_td = tr.find_all("td")
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        if(len(all_td)) :
            
            player_name = all_td[0].text
            player_born = all_td[3].text
            sql = f'SELECT * FROM playerlist WHERE player_name ="{player_name}" and birthday = "{player_born}"'
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            if len(myresult) == 0:
                print(f"Error find playerid of {player_name}")
                """player_height = all_td[4].text
                player_position = all_td[5].text
                href_info = all_td[0].find("a")['href']
                url = "https://www.worldfootball.net"+href_info
                player_adding_info = get_more_player_info(url , player_name)
                print(f"this is new player- {player_name} : {player_born}")
                sql = "INSERT INTO playerlist (player_name, birthday , nationality, img_src, height, weight, foot" \
                      ", position ) VALUES (%s, %s , %s, %s, %s, %s, %s, %s)"
                val = (player_name, player_born,player_adding_info[1],player_adding_info[0], \
                               player_height, player_adding_info[2] \
                               ,player_adding_info[3], player_position)
                mycursor.execute(sql, val)
                mydb.commit()
                player_id = mycursor.lastrowid
                print("new player added")"""

            else:
                player_id = myresult[0][0]
            print(f"-------------{season}-{pageNumber}-{i}th player : id- {player_id} data handling start!-----------")
            sql = f'SELECT * FROM player_career WHERE player_id ="{player_id}"'
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            if len(myresult):
                print(f"{player_id}th data is already added!")
            else:
                href_info = all_td[0].find("a")['href']
                url = "https://www.worldfootball.net"+href_info+"/2/"
                page = requests.get(url , headers={"User-Agent":"Mozilla/5.0"})
                soup = BeautifulSoup(page.content, "html.parser")
                ################################### page url check end ###############################
                ################################### career check start ###############################
                extra_results = soup.find('table', class_="standard_tabelle")

                extra_tr_results = extra_results.find_all("tr")
               
                count = 1
                tr_index = 1
                for tr in extra_tr_results:
                    all_td = tr.find_all("td")
                    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
                    if(len(all_td)) :
                        if (tr_index > 1) and len(all_td) < 2: # no carrer
                            break
                        else: 
                            flag = all_td[0].find('img')['src']
                            league_id = fn_Get_LeagueId(all_td[1].text, all_td[1].find('a')['href'])
                            season_id = fn_Get_SeasonId(all_td[2].text)
                            team_id = fn_Get_TeamId(all_td[3].text)
                            
                            sql = f"INSERT INTO player_career (player_id, flag, league_id, season_id, team_id, matches, goals, started,s_in, s_out, yellow, s_yellow, red ) VALUES ({player_id},'{flag}', {league_id} ,{ season_id}, {team_id}, \
                                {  fn_filter_value(all_td[4].text)}, \
                                { fn_filter_value(all_td[5].text)}, \
                                { fn_filter_value(all_td[6].text)}, \
                                { fn_filter_value(all_td[7].text)}, \
                                { fn_filter_value(all_td[8].text)}, \
                                { fn_filter_value(all_td[9].text)}, \
                                { fn_filter_value(all_td[10].text)}, \
                                { fn_filter_value(all_td[11].text)})"
                            
                            mycursor.execute(sql)
                            mydb.commit()
                            print(f"   added extra new row-{count}")
                            count = count + 1
                    tr_index = tr_index +1
                        
            
            print(f"-------------{season}-{pageNumber}-{i}th player : id- {player_id} : name: {player_name}'s data handling End !-----------")
            i = i+1

def fn_filter_value(str):
    
    if '?' in str:
        return 0
    else: 
        return int(str)
                    
def fn_Get_LeagueId(league_dname, league_extra_info):
    realLeague = league_extra_info.split("/")[2]
    if league_dname == "Bundesliga":
      
        if realLeague == "bundesliga":
            return 8
        if realLeague == "aut-bundesliga":
            return 1
        else:
            sql = f'SELECT league_id FROM league where league_title = "{realLeague}"'  # if league dname's duplicate exists, then search league_title
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            if myresult:
                return myresult[0]
            else:
                sql = f'INSERT INTO league (league_dname , league_title ) VALUES ("{league_dname}, {realLeague}")'
                mycursor.execute(sql)
                mydb.commit()
                print("   -------added new league-"+league_dname + ":"+ realLeague)
                return mycursor.lastrowid
    if league_dname == "Super League":
       # realLeague = league_extra_info.split("/")[2]
        if realLeague == "gre-super-league":
            return 9
        if realLeague == "sui-super-league":
            return 18
        else:
            sql = f'SELECT league_id FROM league where league_title = "{realLeague}"'  # if league dname's duplicate exists, then search league_title
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
            if myresult:
                return myresult[0]
            else:
                sql = f'INSERT INTO league (league_dname , league_title ) VALUES ("{league_dname}, {realLeague}")'
                mycursor.execute(sql)
                mydb.commit()
                print("   -------added new league-"+league_dname + ":"+ realLeague)
                return mycursor.lastrowid
    
    sql = f'SELECT league_id FROM league where league_dname = "{league_dname}"'
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    if myresult:
        return myresult[0]
    else:
        sql = f'INSERT INTO league (league_dname , league_title ) VALUES ("{league_dname}", "{realLeague}")'
        mycursor.execute(sql)
        mydb.commit()
        print("   -------added new league-"+league_dname + ":"+ realLeague)
        return mycursor.lastrowid

def fn_Get_SeasonId(season_title):
    sql = f'SELECT season_id FROM season where season_title = "{season_title}"'
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    if myresult:
        return myresult[0]
    else:
        sql = f'INSERT INTO season (season_title ) VALUES ("{season_title}")'
        mycursor.execute(sql)
        mydb.commit()
        print("   ----------added new season-" + season_title)
        return mycursor.lastrowid

def fn_Get_TeamId(team_name):
    sql = f'SELECT team_id FROM team_list where team_name = "{team_name}"'
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    if myresult:
        return myresult[0]
    else:
        sql = f'INSERT INTO team_list (team_name ) VALUES ("{team_name}")'
        
        mycursor.execute(sql)
        mydb.commit()
        print("   ---------added new team-" + team_name)
        return mycursor.lastrowid

def get_more_player_info(url , player_name):

    page = requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find('div', itemtype="http://schema.org/Person")
    player_img = results.find("img", alt = player_name)["src"]

    player_nation_container = results.find(string = "Nationality:").findNext("td")
    player_nation_container = player_nation_container.find_all("img")
    count = 0
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

def main():
    
   
    for i in range(1, 12):
        insert_player_wholecareer("2014-2015", "hun-nb-i" , i)
    for i in range(1, 9):
        insert_player_wholecareer("2015-2016", "hun-nb-i" , i)
    for i in range(1, 8):
        insert_player_wholecareer("2016-2017", "hun-nb-i" , i)
    for i in range(1, 8):
        insert_player_wholecareer("2017-2018", "hun-nb-i" , i)
    for i in range(1, 9):
        insert_player_wholecareer("2018-2019", "hun-nb-i" , i)

    for i in range(1, 12):
        insert_player_wholecareer("2014-2015", "srb-super-liga" , i)
    for i in range(1, 11):
        insert_player_wholecareer("2015-2016", "srb-super-liga" , i)
    for i in range(1, 11):
        insert_player_wholecareer("2016-2017", "srb-super-liga" , i)
    for i in range(1, 11):
        insert_player_wholecareer("2017-2018", "srb-super-liga" , i)
    for i in range(1, 11):
        insert_player_wholecareer("2018-2019", "srb-super-liga" , i)


if '__main__' == __name__:
    main()





