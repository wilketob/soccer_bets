import re
from urllib import request
import json
#from mysql.connector import MySQLConnection, Error #https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
import pymysql
import sshtunnel #https://stackoverflow.com/questions/21903411/enable-python-to-connect-to-mysql-via-ssh-tunnelling

url_crosstable = 'https://www.fussballdaten.de/bundesliga/kreuztabelle/'
#https://www.fussballdaten.de/bundesliga/1964/kreuztabelle/
config_file="settings.json"

def sql_login(config_file):
    with open(config_file) as f:
        config_data_sql = json.load(f)["sql_server"]
        return config_data_sql

def ssh_login(config_file):
    with open(config_file) as f:
        config_data_ssh = json.load(f)["ssh_server"]
        return config_data_ssh

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

def sql_connect(query,query_type,results_for_db):
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
                            except Exception as e:
                                cursor_data = e
                        cursor_data = cur.fetchall()
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
        except Exception as err:
            print(err)
    else:
        print("Define the routine if no SSH connection is mandatory")

def data_crosstable(url_crosstable):
    url_requested = request.urlopen(url_crosstable)
    html_content = str(url_requested.read().decode('utf-8'))
    return html_content
    #print(url_requested.code)
    #print(html_content)


def score_results():
    re_search_chunk = []
    re_search_chunk = re.findall('>[0-9]:[0-9]<', data_crosstable(url_crosstable))
        return re_search_chunk

def main():
    re_search_chunk = score_results()
    print(re_search_chunk.sort())
    print(type(re_search_chunk))
    set_search_chunk = set(re_search_chunk)
    for a in set_search_chunk:
        print(a.strip('>').strip('<') + ' = ' + str(re_search_chunk.count(a)))

if __name__ == '__main__':
    main()

#URL für Tabellenstände an einem bestimmten Spieltag: https://www.fussballdaten.de/bundesliga/tabelle/1977/2/  (Jahr 2018 = Saison 2016/2017 // 2 = Spieltag)
# URL für Spielergebnisse an einem bestimmten Tag mit Angabe des Tages https://www.fussballdaten.de/bundesliga/2017/4/

#Query what
#
