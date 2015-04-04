






teamStats = {
        
    'Name': 'TEXT',
    'Week': 'DATE',
    'W' : 'INT',
    'L' : 'INT',
    'PTS' : 'INT',
    'PPG' : 'DECIMAL(6, 2)',    
    'Pct' : 'DECIMAL(6, 2)',      
    'OPP_PTS' : 'INT',
    'OPP_PPG' : 'DECIMAL(6, 2)',
    'SCR_MAR' : 'DECIMAL(6, 2)',
    'FGA' : 'INT',
    'FGM' : 'INT',                
    'FG_PERCENTAGE' : 'DECIMAL(6, 2)',
    'OPP_FG'  : 'INT',
    'OPP_FGA' : 'INT',  
    'OPP_FG_PERCENTAGE' : 'DECIMAL(6, 2)',
    'Opp_3FGA' : 'INT', # of course here is the one thing they don't capitalize consitently
    'Opp_3FG' : 'INT',
    '3FG' : 'INT', 
    '3PG' : 'DECIMAL(6, 2)', 
    '3FGA' : 'INT',
    '3FG_PERCENTAGE': 'DECIMAL(6, 2)',
    'FT' : 'INT',
    'FTA' : 'INT',
    'FT_PERCENTAGE' : 'DECIMAL(6, 2)',
    'REB' : 'INT',
    'OPP_REB': 'INT',
    'RPG' : 'DECIMAL(6, 2)',
    'OPP_RPG' : 'DECIMAL(6, 2)',
    'PFPG': 'DECIMAL(6, 2)',
    'REB_MAR' : 'DECIMAL(6, 2)',
    'DQ': 'INT',
    'AST' : 'INT',
    'APG': 'DECIMAL(6, 2)',
    'TURNOVERS' : 'INT',
    "TOPG" : 'DECIMAL(6, 2)',
    'GM': 'INT',
    "BLKS" : 'INT',
    "BKPG" : 'DECIMAL(6, 2)',
    "ST" :  'INT',
    "STPG" : 'DECIMAL(6, 2)',
    'Ratio': 'DECIMAL(6, 2)',
    "Opp_TO" : 'INT',
    "Fouls" : 'INT',
    "PFPG" :'DECIMAL(6, 2)',
    "DQ" : 'INT'
    
}


playerStaticStats = {
    'Name' : 'TEXT',
    'Team' : 'TEXT',

}

playerStats = {
    'Week' : 'DATE',
    'Ht'   : 'DECIMAL(6, 2)',
    'Cl'  : 'TEXT', # year? if so, no idea why it's 'cl'
    'Pos' : 'TEXT', # a player might change what position they play
    'G'   : 'INT',
    'FGM' : 'INT',
    '3FG' : 'INT',
    'FT'  : 'INT',
    'PTS' : 'INT',
    'PPG' : 'DECIMAL(6, 2)',
    'FGM' : 'INT', 
    'FGA' : 'INT', 
    'FG_PERCENTAGE' : 'DECIMAL(6, 2)',
    '3FG' : 'INT',
    '3PG' : 'DECIMAL(6, 2)',
    '3FGA': 'INT',
    '3FG_PERCENTAGE' : 'DECIMAL(6, 2)',
    'FT'  : 'INT',
    'FTA' : 'INT',
    'FT_PERCENTAGE' : 'DECIMAL(6, 2)',
    'REB' :'INT',
    'RPG' : 'DECIMAL(6, 2)',
    'AST' : 'INT',
    'APG' : 'DECIMAL(6, 2)',
    'BLKS' : 'INT',
    'BKPG' : 'DECIMAL(6, 2)',
    'ST' : 'INT',
    'STPG' : 'DECIMAL(6, 2)',
    'AST' : 'INT',
    'TURNOVERS' : 'INT', #this is really 'TO' - but that's a reserved keyword in sql
    'Ratio' : 'DECIMAL(6, 2)'
}




