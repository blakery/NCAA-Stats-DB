
#Purpose: 
Input: csv formatted files of NCAA Basketball statistics
Output: SQL Database of processed statistics

#Requirements:
    PLY Python based Lex-Yacc implementation http://www.dabeaz.com/ply/ply.html
    MySQL
    MySQLdb

#Failure Conditions
 Condition | Action
-----------|----------------
nonexistant resources | exit and display error
improperly formatted file | recover, extract all data possible, and output warning
    
    
#Database Structure
Table Name | Occourance| Content
-----------|-----------|--------
'teams'| Global | a listing of all the teams by name
'TeamName'| one for each team | all of the team's players by name, static stats (ie height)
'TeamNameStats'| one for each team | all of the stats for the team, keyed by week
'PlayerName' | one for each player | the player's stats, keyed by week







