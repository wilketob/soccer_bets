#https://www.anchor.com.au/hosting/support/CreatingAQuickMySQLRelationalDatabase#head-e553653f2d7e592b1cbba9afca44c25cd12f6ee4
from connect_and_run import sql_connect
from datetime import datetime
import re

def create_table_setup(league):
    query = ("CREATE TABLE IF NOT EXISTS db_setup ("
    "setup_date DATE,"
    "table_name VARCHAR(20))"
    " ENGINE = InnoDB") #Alternativ use the `` instead of ' or "
    query_type = query[0:query.find(" ",0)]
    try:
        cursor_data = sql_connect(query,query_type,'')
        print(cursor_data)
    except Exception as e:
        print(e)

def create_table_teams(league):
    query = (f"CREATE TABLE IF NOT EXISTS {league}_teams ("
    "teamid INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (teamid) ,"
    "team VARCHAR(6),"
    "team_name VARCHAR(30)) ENGINE = InnoDB;")
    query_type = query[0:query.find(" ",0)]
    try:
        cursor_data = sql_connect(query,query_type,'')
        print(cursor_data)
    except Exception as e:
        print(e)

def create_table_results(league):
    query = (f"CREATE TABLE IF NOT EXISTS {league}_results ("
    "resultid INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (resultid),"
    "season VARCHAR(9),"
    "matchweek INT NOT NULL,"
    "date VARCHAR (10),"
    "weekday VARCHAR(10),"
    "teamhome VARCHAR (30),"
    "teamguest VARCHAR (30),"
    "scorehome INT,"
    "scoreguest INT) ENGINE = InnoDB;")
    query_type = query[0:query.find(" ",0)]
    try:
        cursor_data = sql_connect(query,query_type,'')
        print(cursor_data)
    except Exception as e:
        print(e)

def create_table_leaguetables(league):
    query = (f"CREATE TABLE IF NOT EXISTS {league}_leaguetables ("
    "leaguetablesid INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (leaguetablesid),"
    "season VARCHAR(9),"
    "date VARCHAR (10),"
    "matchweek INT,"
    "team VARCHAR(30),"
    "rank INT,"
    "points INT,"
    "won INT,"
    "lost INT,"
    "drawn INT,"
    "goalsfor INT,"
    "goalsagainst INT,"
    "goalsdiff VARCHAR(5)) ENGINE = InnoDB;")
    try:
        cursor_data = sql_connect(query,"CREATE",'')
        print(cursor_data)
    except Exception as e:
        print(e)
