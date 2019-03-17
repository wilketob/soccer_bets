import os
import time
from create_table import *
from initial_data import get_initial_data


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
    get_initial_data(league)




if __name__ == '__main__':
    main()
