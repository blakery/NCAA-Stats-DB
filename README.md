
Purpose: 

Input: csv formatted files of NCAA Basketball statistics
Output: SQL Database of processed statistics

Requirements:
       - PLY Python based Lex-Yacc implementation
          http://www.dabeaz.com/ply/ply.html
       - MySQL
       - MySQLdb


Failure Conditions:
    - nonexistant resources : exit and display error
    - improperly formatted file : recover, extract all data possible, 
        and output warning
    
    
Database Structure:
    Table 'teams': a table listing all of the teams by name

    Table 'TeamName' - for each team, a table consisting of a roster listing all of the
            players by name, as well as stats that don't change (ie height)

    Table 'TeamNameStats' - for each team, a table listing all of the stats for the 
            team, keyed by week
     
    Table 'PlayerName' - for each player, a table for each player(by player name), listing
            their stats, keyed by week







