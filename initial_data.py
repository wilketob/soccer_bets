from connect_and_run import data_crosstable

def bl_initial_data():
    start_year = 2017
    end_year = get_year()  + 1
    results_for_db = []
    for every_year in range(start_year,end_year):
        url_crosstable = 'https://www.fussballdaten.de/bundesliga/' + str(start_year) + '/kreuztabelle/'
        re_search_res = []
        re_search_res = re.findall('(title="[0-9]{1,2}. Spieltag)(.+?)</a>', data_crosstable(url_crosstable))
        print("[++++]Search_res: " + str(re_search_res))
        for a in re_search_res:#re_search_dict = set(re_search_chunk)
            matchweek = re.findall('[0-9]{1,2}',a[0])[0]
            date = a[1][2:12]
            if date: #only when date is not Null
                print("Date: " + date)    #ToDo delete if not needed
                weekday = datetime.strptime(date,"%d.%m.%Y").strftime("%A")
                teamhome = a[1][a[1].find(",",2)+2:a[1].find("-",2)-1]
                teamguest = a[1][a[1].find("-",2)+2:a[1].find(",",a [1].find("-",2))]
                scorehome = re.findall('data-toggle=tooltip>(.+?):', a[1])[0]
                scoreguest = re.findall('data-toggle=tooltip>[0-9]{1,2}:(.+?)', a[1])[0]
                results_for_db.append((start_year,matchweek,date,weekday,teamhome,teamguest,scorehome,scoreguest))
        start_year  += 1
    print("[+++]Result of Website scrape: " + str(results_for_db))
    query =("INSERT INTO bl1_results (season,matchweek, date, weekday, teamhome, teamguest, scorehome, scoreguest) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
    query_type = query[0:query.find(" ",0)] #check if INSERT OR SELECT OR ALTER
    try:
        cursor_data = sql_connect(query,query_type,results_for_db) #
        print(cursor_data)
    except Exception as e:
        print(e)

'''
ToDo
Initial: get all the reults of the all matches
check how we can set a marker what matchdayy is last to hook up for upcoming mmmatches
get all the results  of table rankings

create the job for twice a week get the new results

setup a web frontend (Django or try React / bootstrap)

remove the print statementss
comment the code
build the readme.md

check other leagues
'''
