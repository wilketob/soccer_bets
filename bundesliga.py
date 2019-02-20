import re
from urllib import request
import json

url_crosstable = 'https://www.fussballdaten.de/bundesliga/kreuztabelle/'
config_file="settings.json"

def sql_connect(config_file):
    with open(config_file) as f:
        config_data = json.load(f)
        db_server = config_data["db_server"]
        db_name = config_data["db_name"]
        db_user = config_data["db_user"]
        db_pass = config_data["db_pass"]

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
    score_results()
    print(re_search_chunk.sort())
    #print(type(re_search_chunk))
    set_search_chunk = set(re_search_chunk)
    for a in set_search_chunk:
        print(a.strip('>').strip('<') + ' = ' + str(re_search_chunk.count(e)))

if __name__ == '__main__':
    main()

#URL für Tabellenstände an einem bestimmten Spieltag: https://www.fussballdaten.de/bundesliga/tabelle/1977/2/  (Jahr 2018 = Saison 2016/2017 // 2 = Spieltag)
# URL für Spielergebnisse an einem bestimmten Tag mit Angabe des Tages https://www.fussballdaten.de/bundesliga/2017/4/

#Query what
