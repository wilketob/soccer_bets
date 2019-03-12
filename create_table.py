#https://www.anchor.com.au/hosting/support/CreatingAQuickMySQLRelationalDatabase#head-e553653f2d7e592b1cbba9afca44c25cd12f6ee4
from connect_and_run import sql_connect
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
