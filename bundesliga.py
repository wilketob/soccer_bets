import re
from urllib import request
import json
import mysql.connector #https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html


url_crosstable = 'https://www.fussballdaten.de/bundesliga/kreuztabelle/'
config_file="settings.json"

def sql_login(config_file):
    with open(config_file) as f:
        config_data = json.load(f)
        db_server = config_data["db_server"]
        db_name = config_data["db_name"]
        db_user = config_data["db_user"]
        db_pass = config_data["db_pass"]
        return db_server, db_name, db_user, db_pass

def sql_connect():
    db_server, db_name, db_user, db_pass = sql_login(config_file)
    print(db_server)
    try:
        db_connection = mysql.connector.connect(user=db_user,password=db_pass,host=db_server,database=db_name) #EIne Alternative ist die **Option
        return db_connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
#close the connection in your referenced function

def sql_query(ean):
    db_connection = sql_connect()
    cursor = db_connection.cursor()

    query = (f"""SELECT average_price, storage_location_stock FROM plenty_stock 
             WHERE ean IS {ean}""") #Triple quotation marks for multi line strings

    cursor.execute(query)

    for c in cursor:
        print(c)

    db_connection.close()


def data_crosstable(url_crosstable):
    url_requested = request.urlopen(url_crosstable)
    html_content = str(url_requested.read())
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
