import re
from connect_and_run import get_html_content
from connect_and_run import sql_connect
from connect_and_run import build_daily_link
from connect_and_run import get_last_row
from connect_and_run import count_matchweeks
from connect_and_run import build_url
from initial_data import scrape_years


def get_weekly_results(league):
    matchweek = get_last_row('matchweek',league)[0][0]
    season = get_last_row('season',league)[0][0]
    print('### START DEBUG ###')
    print(f'season: {season}')
    print(f'matchweek: {matchweek}')
    print('Type count_matchweeks', count_matchweeks(league, matchweek, season)[0][0])
    print('### END DEBUG ###')
    if (count_matchweeks(league, matchweek, season)[0][0] < 8): # change the '8' to half of qty teams
        print('Running IF')
        url_data = build_url(matchweek,league,season)
        html_data = get_html_content(url_data)
        print(url_data)

    #read day from sportschau and compare what matches are not in db
    elif (matchweek == 34):
        print('Running ELIF')
        print(f'matchweek: {matchweek}')
        print(f'season {season} Typ: {type(season)}')
        season = [int(season) + 1]
        print(f'season {season} Typ: {type(season)}')
        matchweek = 1
        scrape_years(league,season)
        
    else:
        print('Nothing')

def main():
    get_weekly_results('BL1')


if __name__ == '__main__':
    main()

#URL für Tabellenstände an einem bestimmten Spieltag: https://www.fussballdaten.de/bundesliga/tabelle/1977/2/  (Jahr 2018 = Saison 2016/2017 // 2 = Spieltag)
# URL für Spielergebnisse an einem bestimmten Tag mit Angabe des Tages https://www.fussballdaten.de/bundesliga/2017/4/

#Query what
#
