from connect_and_run import sql_connect
from connect_and_run import build_daily_link
from connect_and_run import get_html_content
from connect_and_run import build_url
import re
from datetime import datetime
import html


def ins_table_results(league, data_for_table_results):
    query =(f"INSERT INTO {league}_results (season,matchweek, date, weekday, teamhome, teamguest, scorehome, scoreguest) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
    #query =("INSERT INTO {}_results (season,matchweek,date,weekday,teamhome,teamguest,scorehome,scoreguest) VALUES{};".format(league,str(data_for_table_results)))
    query_type = query[0:query.find(" ",0)] #check if INSERT OR SELECT OR ALTER
    try:
        cursor_data = sql_connect(query,query_type,data_for_table_results) #
        print(cursor_data)
    except Exception as e:
        print(e)


def ins_table_leaguetables(league, data_for_table_leaguetables):
    query = (f"INSERT INTO {league}_leaguetables (season,date,matchweek,team,league_rank,points,won,lost,drawn,goalsfor,goalsagainst,goalsdiff) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    query_type = query[0:query.find(" ",0)] #check if INSERT OR SELECT OR ALTER
    try:
        cursor_data = sql_connect(query,query_type,data_for_table_leaguetables) #
        print(cursor_data)
    except Exception as e:
        print(e)

def get_initial_data(league):
    base_url = 'https://www.sportschau.de/fussball/bundesliga/spieltag/index.html'
    html_data = get_html_content(base_url)
    #html: <option value="1964">1963/1964</option>
    all_years = re.findall('option value="([0-9]{4})">',html_data)
    #TESTCASE - uncomment if you want only a special year:
    #all_years = [2019]
    start_year = all_years[0]
    end_year = all_years[-1]
    #jsp_url, eap_url = build_daily_link()
    scrape_years(league,all_years)


def scrape_years(league,all_years):
    #for every_year in range(start_year,end_year):
    for every_year in all_years:
        print('Ergebnisse der Saison ' + str(every_year))
        url_data_season = build_url(1,league,every_year)
        #url_data_season = 'https://www.sportschau.de/fussball/' + str(jsp_url) + '?_spieltag=1-1&_sportart=fb&_liga=' + str(league) + '&_saison=' + str(every_year) + '&eap=' + str(eap_url)
        print('[++ URL ++] ' + str(url_data_season))
        html_data_season = get_html_content(url_data_season)
        #html: <option value="1-5">5. Spieltag</option>
        all_matchdays = re.findall('value="([0-9]-[0-9]{1,2})',html_data_season)
        scrape_matchdays(league,every_year,all_matchdays)


def scrape_matchdays(league,every_year,all_matchdays):

    for single_matchday in all_matchdays:
        data_for_table_results = []
        data_for_table_leaguetables = []
        print('Ergebnisse des ' + str(single_matchday) + '. Spieltags')
        url_data_matchday = build_url(single_matchday,league,every_year)
        #url_data_matchday = 'https://www.sportschau.de/fussball/' + str(jsp_url) + '?_spieltag=' +str(single_matchday) + '&_sportart=fb&_liga=' + str(league) + '&_saison=' + str(every_year) + '&eap=' + str(eap_url)
        print('[++ URL ++] ' + str(url_data_matchday))
        html_data_matchday = get_html_content(url_data_matchday)
        html_data_matchday = html.unescape(html_data_matchday)
        res_search_html = []
        #separate the matches
        res_search_html = re.findall('<tr class="data">((.|\n|\r)*?)</tr>', html_data_matchday)
        res_table = []
        #separate the result table
        res_table_raw = re.findall('id="hrtabelle((.|\n)*?)</div>',html_data_matchday)
        res_table = re.findall('<tr((.|\n)*?)</tr>',str(res_table_raw))

        for match in res_search_html:
            print(f'[INHALT VON MATCH: {str(match)}]')
            # in current seasons score can be blank, use if to avooid exception
            if len(re.findall('Endstand: </span>([0-9]{1,2}):<',match[0])) > 0:
                matchweek = re.findall('-([0-9]{1,2})',single_matchday)[0] #single_matchday #
                date = re.findall('\d\d\.\d\d\.\d\d\d\d',match[0])[0]
                weekday = datetime.strptime(date,"%d.%m.%Y").strftime("%A")
                base_url = 'https://www.sportschau.de/fussball/bundesliga/spieltag/index.html'
                teamhome = re.findall('scope="row">(.*?) <',match[0])[0]
                teamguest = re.findall('gegen</span>: (.*?)<',match[0])[0]
                scorehome = re.findall('Endstand: </span>([0-9]{1,2}):<',match[0])[0]
                scoreguest = re.findall('zu </span>([0-9]{1,2})',match[0])[0]
                print('hallo')
                print(f'Date: {date}')
                data_for_table_results.append((every_year,matchweek,date,weekday,teamhome,teamguest,scorehome,scoreguest))
                #new try to write the data after each match
                #data_for_table_results = (every_year,matchweek,date,weekday,teamhome,teamguest,scorehome,scoreguest)
            #: whats about the league tables, you can grab it from same Website
            # without parsing the site a 2nd time
        for team_rank in res_table:
            print('Table Results')
            if (len(re.findall('>(\d{1,2})</',str(team_rank))) > 1):
                #get the latest match day as date for table
                #date = re.findall('\d\d\.\d\d\.\d\d\d\d',match[0])[0]
                matchweek = re.findall('>(\d{1,2})</',team_rank[0])[1]
                print(f'matchweek: {matchweek}')
                team = re.findall('spvVerein_[0-9]{1,9}_[0-9]{1,9}">(.*?)<',team_rank[0].replace('<strong>',''))[0]
                print(f'Team {team}')
                league_rank = 1 #re.findall('>(\d{1,2})</',team_rank[0])[0]
                try:
                    points = re.findall('>(\d{1,2})</',team_rank[0])[5]
                except:
                    points = '0'
                won  = re.findall('>(\d{1,2})</',team_rank[0])[2]
                lost = re.findall('>(\d{1,2})</',team_rank[0])[4]
                drawn = re.findall('>(\d{1,2})</',team_rank[0])[3]
                goalsfor = re.findall('spvTorverhaeltnis_[0-9]{1,9}_[0-9]{1,9}">(.*?):',team_rank[0])[0]
                goalsagainst = re.findall('spvTorverhaeltnis_[0-9]{1,9}_[0-9]{1,9}">[0-9]{1,3}:(.*?)<',team_rank[0])[0]
                goalsdiff = re.findall('spvTordifferenz_[0-9]{1,9}_[0-9]{1,9}">(.*?)<',team_rank[0])[0]
                data_for_table_leaguetables.append((every_year,date,matchweek,team,league_rank,points,won,lost,drawn,goalsfor,goalsagainst,goalsdiff))
                print('Data: ', data_for_table_leaguetables)
                #data_for_table_leaguetables = (every_year,date,matchweek,team,league_rank,points,won,lost,drawn,goalsfor,goalsagainst,goalsdiff)


        print("[+++]Result of Website scrape: " + str(type(data_for_table_results)) + str(data_for_table_results))
        ins_table_results(league, data_for_table_results)
        print("[+++]Result of Website scrape: " + str(type(data_for_table_leaguetables)) + str(data_for_table_leaguetables))
        ins_table_leaguetables(league, data_for_table_leaguetables)
    #print("[+++]Result of Website scrape: " + str(data_for_table_results))
    #print(type(data_for_table_results))
    #print(type(data_for_table_leaguetables))
    #return ((data_for_table_results, data_for_table_leaguetables))









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
#                data_for_table_results.append((start_year,matchweek,date,weekday,teamhome,teamguest,scorehome,scoreguest))
#        start_year  += 1
#    print("[+++]Result of Website scrape: " + str(data_for_table_results))
#    query =("INSERT INTO bl1_results (season,matchweek, date, weekday, teamhome, teamguest, scorehome, scoreguest) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
#    query_type = query[0:query.find(" ",0)] #check if INSERT OR SELECT OR ALTER
#    try:
#        cursor_data = sql_connect(query,query_type,data_for_table_results) #
#        print(cursor_data)
##    except Exception as e:
#        print(e)
#
#
#ToDo
#
#SELECT COUNT( matchweek )
#FROM  `BL1_results`
#WHERE  `matchweek` =30
#
#
#change the writing to DB from end of all to end of each year
#make a entry at db_setup which year which league you scraped successful
#in case of restart the setup check what years we already have and start from there
#If a year will be written set league and year
#running setup check what year and leagues exist
#
# Try to work out the exceptions more detailed and
#
#Initial: get all the reults of the all matches
#check how we can set a marker what matchdayy is last to hook up for upcoming mmmatches
#get all the results  of table rankings
#
#create the job for twice a week get the new results
#
#setup a web frontend (Django and try React / bootstrap)
#
#remove the print statementss - there is a status bar for it :-) https://getpocket.com/a/read/2527334297
#comment the code
#build the readme.md
#
#check other leagues
