import re
from urllib import request

url = 'https://www.fussballdaten.de/bundesliga/kreuztabelle/'

url_requested = request.urlopen(url)
html_content = str(url_requested.read())


print(url_requested.code)
print(html_content)
page_content=[]

re_search_chunk = []

re_search_chunk = re.findall('>[0-9]:[0-9]<',html_content)


print(re_search_chunk.sort())
#print(type(re_search_chunk))
a_set = set(re_search_chunk)
for e in a_set:
    print(e.strip('>').strip('<') + ' = ' + str(re_search_chunk.count(e)))


#URL für Tabellenstände an einem bestimmten Spieltag: https://www.fussballdaten.de/bundesliga/tabelle/1977/2/  (Jahr 2018 = Saison 2016/2017 // 2 = Spieltag)
# URL für Spielergebnisse an einem bestimmten Tag mit Angabe des Tages https://www.fussballdaten.de/bundesliga/2017/4/

#Query what