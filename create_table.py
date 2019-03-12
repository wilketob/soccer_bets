#https://www.anchor.com.au/hosting/support/CreatingAQuickMySQLRelationalDatabase#head-e553653f2d7e592b1cbba9afca44c25cd12f6ee4
from bundesliga import sql_connect
from bundesliga import data_crosstable
from datetime import datetime
import re

def create_initial_table():
    query = ("CREATE TABLE IF NOT EXISTS bl1_setup (setup_date DATE) ENGINE = InnoDB") #Alternativ use the `` instead of ' or "
    try:
        cursor_data = sql_connect(query)
        print(cursor_data)
    except Exception as e:
        print(e)

def create_table_teamsBL1():
    query = ("CREATE TABLE IF NOT EXISTS bl1_teams (teamid INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (teamid) ,"
    "team VARCHAR(6),"
    "team_name VARCHAR(30)) ENGINE = InnoDB;")
    try:
        cursor_data = sql_connect(query)
        print(cursor_data)
    except Exception as e:
        print(e)

def create_table_resultsBL1():
    query = ("CREATE TABLE IF NOT EXISTS bl1_results (resultid INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (resultid),"
    "season VARCHAR(9),"
    "matchweek INT NOT NULL,"
    "date VARCHAR (10),"
    "weekday VARCHAR(10),"
    "teamhome VARCHAR (30),"
    "teamguest VARCHAR (30),"
    "scorehome INT,"
    "scoreguest INT) ENGINE = InnoDB;")
    try:
        cursor_data = sql_connect(query,"CREATE",'')
        print(cursor_data)
    except Exception as e:
        print(e)

def create_table_leaguetablesBL1():
    query = ("CREATE TABLE IF NOT EXISTS bl1_leaguetables (leaguetablesid INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (leaguetablesid),"
    "season VARCHAR(9),"
    "date DATE,"
    "matchweek INT,"
    "team VARCHAR(4),"
    "rank INT,"
    "points INT,"
    "won INT,"
    "lost INT,"
    "drawn INT,"
    "goalsfor INT,"
    "goalsagainst INT,"
    "goalsdiff INT) ENGINE = InnoDB;")
    try:
        cursor_data = sql_connect(query)
        print(cursor_data)
    except Exception as e:
        print(e)

#get_year ask for the current year for use as placeholder in url request for kreuztabelle
def get_year():
    yy = datetime.now().year
    wd = datetime.now().strftime("%A")
    #a hat das Format 01.01.1990 15:30 (aus der Kreuztabelle) und wird mit strptime in das datetime format umgewaldelt
    #aus demm man denn mit strftime alle einzelenn Dtaen ziehen kann wie z:b: %A = Wochentag
    wd2 = datetime.strptime("09.01.1978 15:00","%d.%m.%Y %H:%M").strftime('%A')
    if datetime.now().month <= 6:
        return yy
    else:
        return yy + 1

def bl_initial_data():
    start_year = 2017
    end_year = get_year()  + 1
    results_for_db = []
    for every_year in range(start_year,end_year):
        url_crosstable = 'https://www.fussballdaten.de/bundesliga/' + str(start_year) + '/kreuztabelle/'
        re_search_res = []
        re_search_res = re.findall('(title="[0-9]{1,2}. Spieltag)(.+?)</a>', data_crosstable(url_crosstable))
        print("[++++]Search_res: " + str(re_search_res))
        for a in re_search_res:#re_search_dict = set(re_search_chunk)
            matchweek = re.findall('[0-9]{1,2}',a[0])[0]
            date = a[1][2:12]
            if date: #only when date is not Null
                print("Date: " + date)    #ToDo delete if not needed
                weekday = datetime.strptime(date,"%d.%m.%Y").strftime("%A")
                teamhome = a[1][a[1].find(",",2)+2:a[1].find("-",2)-1]
                teamguest = a[1][a[1].find("-",2)+2:a[1].find(",",a [1].find("-",2))]
                scorehome = re.findall('data-toggle=tooltip>(.+?):', a[1])[0]
                scoreguest = re.findall('data-toggle=tooltip>[0-9]{1,2}:(.+?)', a[1])[0]
                results_for_db.append((start_year,matchweek,date,weekday,teamhome,teamguest,scorehome,scoreguest))
        start_year  += 1
    print("[+++]Result of Website scrape: " + str(results_for_db))
    query =("INSERT INTO bl1_results (season,matchweek, date, weekday, teamhome, teamguest, scorehome, scoreguest) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
    query_type = query[0:query.find(" ",0)] #check if INSERT OR SELECT OR ALTER
    try:
        cursor_data = sql_connect(query,query_type,results_for_db) #
        print(cursor_data)
    except Exception as e:
        print(e)

'''
ToDo
Initial: get all the reults of the all matches
check how we can set a marker what matchdayy is last to hook up for upcoming mmmatches
get all the results  of table rankings

create the job for twice a week get the new results

setup a web frontend (Django or try React / bootstrap)

remove the print statementss
comment the code
build the readme.md

check other leagues
'''
