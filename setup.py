import os
import time
from create_table import *
from initial_data import get_initial_data
from initial_data import scrape_matchdays
from initial_data import scrape_years
from initial_data import ins_table_results
from initial_data import ins_table_leaguetables

#BL1: https://www.sportschau.de/fussball/bundesliga/spieltag/index.html
#BL2: https://www.sportschau.de/fussball/bundesliga2/spieltag/index.html
#PremierLeague: https://www.sportschau.de/fussball/international/england/index.html
#Primera Division: https://www.sportschau.de/fussball/international/spanien/index.html
#Serie A: https://www.sportschau.de/fussball/international/italien/index.html


def main():
    for i in range(0,3):
        os.system('cls' if os.name == "nt" else 'clear')
        league = input("Willkommen bei der Soccer Bet App\n"
        "[BL1] 1. Bundesliga\n"
        "[BL2] 2. Bundesliga\n"
        "Für welche Liga willst Du das Setup starten   ")
        if league not in ['BL1','BL2']:
            print('Falsche Eingabe')
            time.sleep(1)
        else:
            print('Buenos dias, Don')
            break
    #Create the tables (if not exist)
    create_table_setup(league)
    create_table_results(league)
    create_table_leaguetables(league)

    #Run the initial Scrape of the leagues
    #data_for_table_results, data_for_table_leaguetables = get_initial_data(league)
    get_initial_data(league)

    #testcase for single matchdays
    #data_for_table_results, data_for_table_leaguetables = scrape_matchdays(league,[1,2,3],2018)

    #testcase for single all_years
    #data_for_table_results, data_for_table_leaguetables = scrape_years(league,[2018,2019])

    type(data_for_table_results) #fr debug
    type(data_for_table_leaguetables) #for debug

    #Write the data to the DB
    #ins_table_results(league, data_for_table_results)
    #ins_table_leaguetables(league, data_for_table_leaguetables)

    print('[+++] Setup successful')


if __name__ == '__main__':
    main()
