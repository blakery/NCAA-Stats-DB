
#Purpose: 
NCAA makes all of its statistics available online. Unfortunately, they're stored 
in inconsistent, hard to manage formats. This program, when passed a file or 
directory name as a cl argument, will extract any NCAA Men's Basketball stats 
from csv formated files, and store them in a mysql database.



#Requirements:
    MySQL
    MySQLdb
    Tkiter (Python Tk interface)

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







