import xlrd
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="soccer"
)

mycursor = mydb.cursor()

def switch_Month(argument):
    switcher = {
      "Jan": "01",
      "Feb": "02",
      "Mar": "03",
      "Apr": "04",
      "May": "05",
      "Jun": "06",
      "Jul": "07",
      "Aug": "08",
      "Sep": "09",
      "Oct": "10",
      "Nov": "11",
      "Dec": "12",
      
       
    }
    return switcher.get(argument, "null")
def switch_season(argument):
    switcher = {
      "2014-2015": 1,
      "2015-2016": 2,
      "2016-2017": 3,
      "2017-2018": 4,
      "2018-2019": 5,
        "2014": 6,
        "2015": 7,
        "2016": 8,
        "2017": 9,
        "2018": 10,
        "2019": 11,
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
        "bul-parva-liga" : 2 , 
        "cze-1-fotbalova-liga": 3,      #Chezch
        "cze-gambrinus-liga": 3,
        "cro-1-hnl": 4 ,          #Croatia
        "hun-nb-i": 10,     #Hungary
        "hun-nb1": 10,
        "hun-otp-liga":10,
        "srb-super-liga": 15    #Serbia
    }
    return switcher.get(argument, "null")



def save_DB(source_path, league,startfrom,Endto):
    loc = (source_path) 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)
    for i in range(startfrom,Endto):

        yy = str((int)(sheet.cell_value(i, 0)))
        mm = switch_Month(sheet.cell_value(i, 1))       
        dd = str((int)(sheet.cell_value(i, 2)))
        if(len(dd) < 2):
            dd = '0'+dd
        date = dd+ '/'+ mm + '/' + yy

        season = str(sheet.cell_value(i, 9))
        home_team_name = (sheet.cell_value(i, 10))
        away_team_name = (sheet.cell_value(i, 11))

        print(f"{i+1}th row's data - {date, season, home_team_name, away_team_name}")

        sql = f"SELECT * FROM season_match_plan AS a " \
            f"INNER JOIN season AS b ON a.`season_id` = b.`season_id` " \
            f"INNER JOIN team_list c ON a.`home_team_id` = c.`team_id` " \
            f"INNER JOIN team_list d ON a.`away_team_id` = d.`team_id` " \
            f"WHERE a.`date` = '{date}' AND a.league_id = {switch_league(league)} AND c.`team_name_odd` = '{home_team_name}' AND d.`team_name_odd` = '{away_team_name}'"
        
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if(len(myresult) !=1 ):
            print("Error! Reading id from DB ")
        else:
            
            sql = f"update season_match_plan set wd_1 = '{sheet.cell_value(i, 18)}', wd_x = '{sheet.cell_value(i, 20)}' , wd_2 ='{sheet.cell_value(i, 22)}', `AH_2.5_1`='{sheet.cell_value(i, 46)}', `AH_2.5_2` = '{sheet.cell_value(i, 48)}', `AH_2.25_1` = '{sheet.cell_value(i, 50)}', `AH_2.25_2`  = '{sheet.cell_value(i, 52)}', `AH_2_1` = '{sheet.cell_value(i, 54)}', `AH_2_2` = '{sheet.cell_value(i, 56)}', \
                  `AH_1.75_1` = '{sheet.cell_value(i, 58)}', `AH_1.75_2` = '{sheet.cell_value(i, 60)}', `AH_1.5_1` = '{sheet.cell_value(i, 62)}',`AH_1.5_2` = '{sheet.cell_value(i, 64)}',`AH_1.25_1` = '{sheet.cell_value(i, 66)}', `AH_1.25_2` = '{sheet.cell_value(i, 68)}',`AH_1_1` = '{sheet.cell_value(i, 70)}', `AH_1_2` = '{sheet.cell_value(i, 72)}', `AH_0.75_1` = '{sheet.cell_value(i, 74)}', `AH_0.75_2` = '{sheet.cell_value(i, 76)}',`AH_0.5_1` = '{sheet.cell_value(i, 78)}', `AH_0.5_2` = '{sheet.cell_value(i, 80)}', \
                  `AH_0.25_1` = '{sheet.cell_value(i, 82)}', `AH_0.25_2` = '{sheet.cell_value(i, 84)}', `AH_0_1` = '{sheet.cell_value(i, 86)}', `AH_0_2` = '{sheet.cell_value(i, 88)}', `AH+0.25_1` ='{sheet.cell_value(i, 90)}', `AH+0.25_2` = '{sheet.cell_value(i, 92)}', `AH+0.5_1` = '{sheet.cell_value(i, 94)}', `AH+0.5_2` = '{sheet.cell_value(i, 96)}', `AH+0.75_1` = '{sheet.cell_value(i, 98)}', `AH+0.75_2` = '{sheet.cell_value(i, 100)}', `AH+1_1` = '{sheet.cell_value(i, 102)}', `AH+1_2` = '{sheet.cell_value(i, 104)}', \
                  `over+2.0` = '{sheet.cell_value(i, 161)}', `under+2.0` = '{sheet.cell_value(i, 163)}',`over+2.25` = '{sheet.cell_value(i, 165)}', `under+2.25` = '{sheet.cell_value(i, 167)}', `over+2.5` = '{sheet.cell_value(i, 169)}', `under+2.5` = '{sheet.cell_value(i, 171)}', `over+3.0` = '{sheet.cell_value(i, 181)}', `under+3.0` = '{sheet.cell_value(i, 183)}', `over+3.5` = '{sheet.cell_value(i, 185)}', `under+3.5` ='{sheet.cell_value(i, 187)}' \
                  where match_id = '{ myresult[0][0] }'"

            print(f"      id is {myresult[0][0]}")
          
            mycursor.execute(sql)
            mydb.commit()
            print("     Successfully Inserted!")



save_DB("Betting Odds Data_Filtered_England.xlsx", "eng-premier-league", 1,  3421)   #index should be real count +1 eg: Englnad: 3421



