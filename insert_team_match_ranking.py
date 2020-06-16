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

def insert_team_rankings():

  sql = f"SELECT  season_id, league_id, team_id , info_id FROM season_league_team_info"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  for i in range(910, 1588):
      season_id = myresult[i][0]
      league_id = myresult[i][1]
      team_id = myresult[i][2]
      info_id = myresult[i][3]

      # print(season_id,league_id, team_id)
      h_mp = h_w = h_d = h_l = h_f = h_a = 0
      a_mp = a_w = a_d = a_l = a_f = a_a = 0
      t_mp = t_w = t_d = t_l = t_f = t_a = 0
      D = P = 0

      sql = f"select total_home_score, total_away_score from season_match_plan where season_id = {season_id} and league_id = {league_id} and home_team_id={team_id}"
      mycursor.execute(sql)
      team_match_results = mycursor.fetchall()
      for match in team_match_results:
        h_mp += 1
        if (match[0] > match[1]):
          h_w += 1
        elif (match[0] == match[1]):
          h_d += 1
        else:
          h_l += 1
        h_f += match[0]
        h_a += match[1]
      #print(h_mp, h_w, h_d, h_l, h_f, h_a)
      ########## get home data end #####################
      sql = f"select total_home_score, total_away_score from season_match_plan where season_id = {season_id} and league_id = {league_id} and away_team_id={team_id}"
      mycursor.execute(sql)
      team_match_results = mycursor.fetchall()
      for match in team_match_results:
        a_mp += 1
        if (match[0] > match[1]):
          a_l += 1
        elif (match[0] == match[1]):
          a_d += 1
        else:
          a_w += 1
        a_a += match[0]
        a_f += match[1]
      #print(a_mp, a_w, a_d, a_l, a_f, a_a)
      ########## get AWAY data end #####################
      t_mp = h_mp + a_mp
      t_w = h_w + a_w
      t_d = h_d + a_d
      t_l = h_l + a_l
      t_f = h_f + a_f
      t_a = h_a + a_a
      D = t_f - t_a
      P = t_w *3 + t_d

      ########## get Total data end #####################
      PPG = round(P/t_mp , 2) 
      HPPG = round((h_w*3 + h_d)/h_mp, 2)
      H_percent = str(round((h_w / h_mp * 100))) + "%"
      HG = h_f
      HGPG = round(h_f/h_mp,2)
      HRS = HPPG + HGPG
      H_ranking = "H" + str(int(HRS)+1)

      APPG = round((a_w*3 + a_d)/a_mp, 2)
      A_percent = str(round((a_w / a_mp * 100))) + "%"
      AG = a_f
      AGPG = round(a_f/a_mp,2)
      ARS = APPG + AGPG
      A_ranking = "A" + str(int(ARS)+1)

      print(t_mp,t_w, t_d, t_l,t_f, t_a,h_mp,h_w, h_d, h_l,h_f, h_a, a_mp,a_w, a_d, a_l, a_f, a_a,D, P, PPG, HPPG, H_percent,HG, HGPG, HRS, APPG, A_percent,AG, AGPG,ARS, H_ranking, A_ranking)
      #sql = "update season_league_team_info set t_mp = %d ,t_w, t_d, t_l,t_f, t_a,h_mp,h_w, h_d, h_l,h_f, h_a, a_mp,a_w, a_d, a_l, a_f, a_a,D, P, PPG, HPPG, H%,HG, HGPG, HRS, APPG, A%,AG, AGPG,ARS, H_ranking, A_ranking  where info_id"
      sql = f"update season_league_team_info set t_mp = {t_mp} ,t_w = {t_w}, t_d = {t_d}, t_l = {t_l},t_f = {t_f}, \
        t_a = {t_a},h_mp = {h_mp},h_w = {h_w}, h_d = {h_d}, h_l = {h_l},h_f = {h_f}, h_a = {h_a}, a_mp = {a_mp}, \
          a_w = {a_w}, a_d = {a_d}, a_l = {a_l}, a_f = {a_f}, a_a = {a_a},D = {D}, P={P}, PPG={PPG}, HPPG={HPPG}, \
          H_percent = '{H_percent}', HG={HG}, HGPG={HGPG}, HRS = {HRS}, APPG={APPG}, A_percent = '{A_percent}',AG={AG}, \
            AGPG={AGPG},ARS = {ARS}, H_ranking = '{H_ranking}', A_ranking ='{A_ranking}' \
        where info_id = {info_id}"

      mycursor.execute(sql)
      mydb.commit()
      print(f"-------------------------One row -{info_id} - updated-------------------")
  print("-------------------end-------------------------------------")
insert_team_rankings()