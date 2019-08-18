# soccer_bets
Become #1 at kicktipp with analyzing historical soccer data from bundesliga and try to forecast the next matches

This software is written in python

Modules used in python
re
request
flask or django for output
mysql

TODO
Get all results from Bundesliga (1st division) and store it to a database.
	Make a table for teams and their shortages: teamid=1 team=fch teamname=FC Hansa Rostock
	Make a table for results: resultid=1,saison=2017/2018, day=18, teamhome=1, teamguest=2 (from table teams), goalshome=1,goalsguest=0,weekday=saturday,date=20.12.2017
Run twice a week (Monday 10pm and Wednesday10pm) and collect new results
logic: for every upcoming game make a forecast based on earlier games and results:
	how were the results based on the same teams, same places in game table, same game days, same win/lose scores, same goal scores
	find a balance of the logic above to make the forecast a precise as possible ;-)
