from connect_and_run import sql_connect
from worker import build_daily_link
from connect_and_run import get_html_content
import re
from datetime import datetime
import html

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

def get_initial_data(league):
    base_url = 'https://www.sportschau.de/fussball/bundesliga/spieltag/index.html'
    html_data = get_html_content(base_url)
    #html: <option value="1964">1963/1964</option>
    all_years = re.findall('option .*? value="([0-9]{4})">',html_data)
    #TESTCASE:
    #all_years = [1964,1965]
    start_year = all_years[0]
    end_year = all_years[-1]
    results_for_db = []
    jsp_url, eap_url = build_daily_link()

    #for every_year in range(start_year,end_year):
    for every_year in all_years:
        print('Ergebnisse der Saison ' + str(every_year))
        url_data_season = 'https://www.sportschau.de/fussball/' + str(jsp_url) + '?_spieltag=1-1&_sportart=fb&_liga=' + str(league) + '&_saison=' + str(every_year) + '&eap=' + str(eap_url)
        print('[++ URL ++] ' + str(url_data_season))
        html_data_season = get_html_content(url_data_season)
        #html: <option value="1-5">5. Spieltag</option>
        all_matchdays = re.findall('value="([0-9]-[0-9]{1,2})',html_data_season)
        first_matchday = all_matchdays[0]
        last_matchday = all_matchdays[-1]

        for single_matchday in all_matchdays    :
                print('Ergebnisse des ' + str(single_matchday) + '. Spieltags')
                url_data_matchday = 'https://www.sportschau.de/fussball/' + str(jsp_url) + '?_spieltag=' +str(single_matchday) + '&_sportart=fb&_liga=' + str(league) + '&_saison=' + str(every_year) + '&eap=' + str(eap_url)
                print('[++ URL ++] ' + str(url_data_matchday))
                html_data_matchday = get_html_content(url_data_matchday)
                html_data_matchday = html.unescape(html_data_matchday)
                res_search_html = []
                res_search_html = re.findall('<tr class="data">((.|\n|\r)*?)</tr>', html_data_matchday)

                for match in res_search_html:
                    print('[INHALT VON MATCH:] '+ str(match))
                    matchweek = re.findall('-([0-9]{1,2})',match[0])[0]
                    date = re.findall('\d\d\.\d\d\.\d\d\d\d',match[0])[0]
                    weekday = datetime.strptime(date,"%d.%m.%Y").strftime("%A")
                    teamhome = re.findall('scope="row">(.*?) <',match[0])[0]
                    teamguest = re.findall('gegen</span>: (.*?)<',match[0])[0]
                    # in current seasons score can be blank, use if to avooid exception
                    if re.findall('Endstand: </span>([0-9]{1,2}):<',match[0])[0]:
                        scorehome = re.findall('Endstand: </span>([0-9]{1,2}):<',match[0])[0]
                        scoreguest = re.findall('zu </span>([0-9]{1,2})<',match[0])[0]
                        results_for_db.append((start_year,matchweek,date,weekday,teamhome,teamguest,scorehome,scoreguest))

    print("[+++]Result of Website scrape: " + str(results_for_db))
    query =(f"INSERT INTO {league}_results (season,matchweek, date, weekday, teamhome, teamguest, scorehome, scoreguest) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
    query_type = query[0:query.find(" ",0)] #check if INSERT OR SELECT OR ALTER
    try:
        cursor_data = sql_connect(query,query_type,results_for_db) #
        print(cursor_data)
    except Exception as e:
        print(e)

#OLD FUnction from fussballdata
#re_search_res = []
#        re_search_res = re.findall('(title="[0-9]{1,2}. Spieltag)(.+?)</a>', html_data))
#        print("[++++]Search_res: " + str(re_search_res))
#        for a in re_search_res:#re_search_dict = set(re_search_chunk)
#            matchweek = re.findall('[0-9]{1,2}',a[0])[0]
#            date = a[1][2:12]
#            if date: #only when date is not Null
#                print("Date: " + date)    #ToDo delete if not needed
#                weekday = datetime.strptime(date,"%d.%m.%Y").strftime("%A")
#                teamhome = a[1][a[1].find(",",2)+2:a[1].find("-",2)-1]
#                teamguest = a[1][a[1].find("-",2)+2:a[1].find(",",a [1].find("-",2))]
#                scorehome = re.findall('data-toggle=tooltip>(.+?):', a[1])[0]
#                scoreguest = re.findall('data-toggle=tooltip>[0-9]{1,2}:(.+?)', a[1])[0]
#                results_for_db.append((start_year,matchweek,date,weekday,teamhome,teamguest,scorehome,scoreguest))
#        start_year  += 1
#    print("[+++]Result of Website scrape: " + str(results_for_db))
#    query =("INSERT INTO bl1_results (season,matchweek, date, weekday, teamhome, teamguest, scorehome, scoreguest) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
#    query_type = query[0:query.find(" ",0)] #check if INSERT OR SELECT OR ALTER
#    try:
#        cursor_data = sql_connect(query,query_type,results_for_db) #
#        print(cursor_data)
##    except Exception as e:
#        print(e)
#
#
#ToDo
#Initial: get all the reults of the all matches
#check how we can set a marker what matchdayy is last to hook up for upcoming mmmatches
#get all the results  of table rankings
#
#create the job for twice a week get the new results
#
#setup a web frontend (Django or try React / bootstrap)
#
#remove the print statementss
#comment the code
#build the readme.md
#
#check other leagues
