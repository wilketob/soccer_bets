#https://www.anchor.com.au/hosting/support/CreatingAQuickMySQLRelationalDatabase#head-e553653f2d7e592b1cbba9afca44c25cd12f6ee4
from bundesliga import sql_connect

def initial_table():
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
    "date DATE,"
    "weekday VARCHAR(2),"
    "teamhome VARCHAR (4),"
    "teamguest VARCHAR (4),"
    "scorehome INT,"
    "scoreguest INT) ENGINE = InnoDB;")
    try:
        cursor_data = sql_connect(query)
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
