import json
#from mysql.connector import MySQLConnection, Error #https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
import pymysql
import sshtunnel #https://stackoverflow.com/questions/21903411/enable-python-to-connect-to-mysql-via-ssh-tunnelling
from urllib import request
import re
from urllib.parse import quote_plus

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


def get_html_content(url):
    #url_requested = request.urlopen(url)
    url_requested = request.Request(url)
    url_requested.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    req = request.urlopen(url_requested)
    html_content = str(req.read().decode('utf-8'))
    return html_content

def build_daily_link():
    url_data = "https://www.sportschau.de/fussball/bundesliga/spieltag/index.html"
    jsp_url = re.findall('<form action="/fussball/(.*?)"',get_html_content(url_data))
    eap_url = re.findall('<input name="eap" type="hidden" value="(.*?)" />',get_html_content(url_data))
    return jsp_url[0], quote_plus(eap_url[0])

def build_url(matchweek,league,season):
    jsp_url, eap_url = build_daily_link()
    return str('https://www.sportschau.de/fussball/' + str(jsp_url) + '?_spieltag=' + str(matchweek) + '&_sportart=fb&_liga=' + str(league) + '&_saison=' + str(season) + '&eap=' + str(eap_url))

def score_results(): # not in use function to get all data from crosstable
    url_crosstable = 'https://www.fussballdaten.de/bundesliga/kreuztabelle/'
    re_search_chunk = []
    re_search_chunk = re.findall('>[0-9]:[0-9]<', get_html_content(url_crosstable))
    return re_search_chunk

def get_last_row(field,league):
    query = (f"SELECT {field} FROM {league}_results ORDER BY resultid DESC LIMIT 1")
    query_type = query[0:query.find(" ",0)]
    print(query)
    try:
        return sql_connect(query,query_type,'')
    except Exception as e:
        print(e)

def count_matchweeks(league,matchweek,season):
    query = (f"SELECT COUNT(matchweek) FROM {league}_results WHERE matchweek = {matchweek} AND season = {season}")
    query_type = query[0:query.find(" ",0)] #check if INSERT OR SELECT OR ALTER
    try:
        qty_matches = sql_connect(query,query_type,'')
        return qty_matches
    except Exception as e:
        print(e)


def sql_login(config_file):
    with open(config_file) as f:
        config_data_sql = json.load(f)["sql_server"]
        return config_data_sql

def ssh_login(config_file):
    with open(config_file) as f:
        config_data_ssh = json.load(f)["ssh_server"]
        return config_data_ssh

def sql_connect(query,query_type,results_for_db):
    config_file="settings.json"
    config_data_sql = sql_login(config_file)
    config_data_ssh = ssh_login(config_file)
    print('[+] Connect to DB server: ' + config_data_sql["host"])
    if config_data_ssh["db_access"] == "ssh":
        print('[+] SQL Connect over SSH tunnel')
        try:
            with sshtunnel.SSHTunnelForwarder(
                    (config_data_ssh["ssh_host"], int(config_data_ssh["ssh_port"])),
                    ssh_username=config_data_ssh["ssh_user"],
                    ssh_password=config_data_ssh["ssh_pass"],
                    remote_bind_address=(config_data_ssh["remote_bind_address"], int(config_data_ssh["remote_bind_port"])),
                    local_bind_address=(config_data_ssh["local_bind_address"],int(config_data_ssh["local_bind_port"]))
            ) as tunnel:
                print('[+] Content of tunnel: ' + str(tunnel))
        except Exception as err:
            print(err)
    else:
        print("Connect direct - no SSH connection")

    print("[+] Try the db_connection")

    db_connection = pymysql.connect(**config_data_sql) #**config.... means use the dictionary
    print("[+] DB COnnection: " + str(db_connection))
    try:
        cur = db_connection.cursor()
        #cursor = db_connection.cursor()
        if len(results_for_db) > 1:
            print('[+] Query Many wird ausgeührt: ' + query)
            cur.executemany(query,results_for_db)
        if (query_type == "ALTER") or (query_type == "INSERT"):
            try:
                print('[+] Execute Commit')
                db_connection.commit()
                cursor_data = cur.fetchall()
            except Exception as e:
                cursor_data = e
        else:
            cur.execute(query)
            if (query_type == "ALTER") or (query_type == "INSERT"):
                try:
                    cur.commit()
                    cursor_data = cur.fetchall()
                except Exception as e:
                    cursor_data = e
            cursor_data = cur.fetchall()
    except Exception as e:
        print(e)
    db_connection.close()
    print('[+] db connection closed')
    return cursor_data

def sql_query(ean):
    #Routine for testing the sl_connect routine
    results_for_db = [] #placeholder for multi values
    query = (f"""SELECT average_price, storage_location_stock FROM plenty_stock
             WHERE ean LIKE '{ean}'""") #Triple quotation marks for multi line strings

    query1 =("SELECT bl1_leaguetables.season,bl1_results.weekday "
            "FROM bl1_leaguetables,bl1_results "
            "WHERE bl1_leaguetables.team = bl1_results.teamhome;")

    cursor_result = sql_connect(query1,"SELECT",results_for_db)

    for c in cursor_result:
        print('[+] Result of query: ' + str(c))
