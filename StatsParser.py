import ply.yacc as yacc
import StatsLexer
from StatsLexer import tokens

g_columns=None
g_date=None


def p_top_level(p):
    '''top_level : section top_level
                 | section
                 | junk top_level  
                 | junk
    '''

# We don't really care about anything not enclosed in quotes except the date,
# but the necessary operations are handled in date's rule
def p_junk(p): '''junk : date 
                       | NEWLINE
                       | WORD
                       | number
                       | DASH'''            


def p_date(p): 
    '''date : INTEGER SLASH INTEGER SLASH INTEGER'''
    global g_date      
    # format to be recognizable to mysql
    g_date = p[5] + "/" + p[1] + "/" + p[3]
    


# section is just a wrapper for a finished block, 
# in order to do operations on the completed block
def p_section(p):
    '''section : block'''
    global g_columns
    g_columns = p[1][0]
    p[1] = p[1][1:]
    p[0] = p[1]
    print(g_columns)
    for i in p[0]:
        print(i)


def p_block(p):
    '''block : ranking_line 
             | ranking_line block
             | ranking_line WORD NEWLINE block
    '''
    if(len(p) == 2):
        p[0] = [p[1]]
    elif(len(p) == 5):
        p[0] = [p[1]]
        p[0].extend(p[4])
    else: 
        p[0] = [p[1]]
        p[0].extend(p[2])



def p_ranking_line(p):
    '''ranking_line : value NEWLINE
                    | value DELIM ranking_line
    '''
    if(len(p) == 3) : p[0] = [p[1]]
    elif(len(p) ==4) : 
        p[0] = [p[1]]
        p[0].extend(p[3])
        

        
def p_value(p):
    '''value : QUOTE QUOTE
             | QUOTE number QUOTE
             | QUOTE team_name QUOTE
             | QUOTE WORD QUOTE
             | QUOTE WORD WORD QUOTE
             | QUOTE INTEGER WORD QUOTE
             | QUOTE integer DASH integer QUOTE
    '''
    if(len(p) == 3): p[0] = None
    elif(len(p) == 4): p[0] = p[2]
    elif(len(p) == 5) : 
        # allow for '3PT', '3FG', and the like in column titles
        if(p[2] == '3'):
            p[0] = p[2] + p[3]
        else:
            p[0] = p[2] + "_" + p[3]
    elif(len(p) == 6) : p[0] = (p[2], p[4])

def p_team_name(p):
    '''team_name : WORD
                 | WORD team_name
                 | team_name TEAM_STATE
    '''
    if(len(p) == 2) : p[0] = p[1]
    elif(len(p) == 3) : p[0] = p[1] + "_" + p[2]


def p_number(p):
    '''number : integer
              | decimal'''
    p[0] = p[1]

              
def p_integer(p):
    '''integer : INTEGER 
               | DASH INTEGER''' # negative
    if(len(p) == 2):
        p[0] = int(p[1]) #p[1]#
    elif(len(p)== 3):
        p[0] = int(p[1] + p[2]) #p[1] + p[2]#


def p_decimal(p):
    '''decimal : DECIMAL
                | DASH DECIMAL''' # negative
    if(len(p) == 2):
        p[0] = float(p[1]) #p[1]
    elif(len(p)== 3):
        p[0] = float(p[1] + p[2])
              

########### END OF GRAMMAR RULES ########################



def p_error(p):
    print ("Syntax Error: %s" % p)


def processFile(fp):
    StatsLexer.setUpLex(fp)
    parser = yacc.yacc()
    finished = parser.parse()



