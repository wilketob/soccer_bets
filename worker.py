import re
from connect_and_run import get_html_content
from connect_and_run import sql_connect
from urllib.parse import quote_plus


def build_daily_link():
    url_data = "https://www.sportschau.de/fussball/bundesliga/spieltag/index.html"
    jsp_url = re.findall('<form action="/fussball/(.*?)"',get_html_content(url_data))
    eap_url = re.findall('<input name="eap" type="hidden" value="(.*?)" />',get_html_content(url_data))
    return jsp_url[0], quote_plus(eap_url[0])

def score_results():
    url_crosstable = 'https://www.fussballdaten.de/bundesliga/kreuztabelle/'
    re_search_chunk = []
    re_search_chunk = re.findall('>[0-9]:[0-9]<', get_html_content(url_crosstable))
    return re_search_chunk

def main(): #noch als Testfunktion für RE und requesst
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
