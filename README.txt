
Purpose: 

Input: csv formatted files of NCAA Basketball statistics
Output: SQL Database of processed statistics

Requirements:
    Python
       - PLY (
          Python based Lex-Yacc implementation
          http://www.dabeaz.com/ply/ply.html
          )
       - MySQLdb

    MySQL




Failure Conditions:
    nonexistant resources : exit and display error
    improperly formatted file : recover, extract all data possible, 
        and output warning
    
    
Database Structure:
    Table 'teams': a table listing all of the teams by name
    
    for each team:
        Table 'TeamName' - a table consisting of a roster listing all of the
            players by name, as well as stats that don't change (ie height)
        Table 'TeamNameStats' - a table listing all of the stats for the 
            team, keyed by week
    
    for each player: 
        Table 'PlayerName' -  a table for each player(by player name), listing
            their stats, keyed by week

    

|------------|   
|table: teams|
|------------|
| team names |
|------------|


|------------------------|
|   table: TeamStats     |
|------------------------|
|team name | week | stats|
|------------------------|
*** What about the fact that it will most often be necessary to interact with a years
    worth of data at a time?
    solution: SELECT * WHERE name == team_name AND YEAR(week) == desired_year

|-------------------------------------------|
|   table team (roster for a single team)   |
|-------------------------------------------|
| player name | static stats (ht.) | yrs 1-4|
|-------------------------------------------|
*** What about the fact that there are different years in question?
    A single player will only be on a team for a max of 4 years.
    \-> maybe start year and n years?



|---------------------|
|   table: player     |
|---------------------|
| name | week | stats |
|---------------------|







