import ply.lex as lex



tokens = [ 
    'DELIM',
    'NEWLINE',    
    'INTEGER',
    'DECIMAL',
    'QUOTE',
    'WORD',
    'TEAM_STATE',  
    'DASH',
    'SLASH'
]



t_DECIMAL = r'\d+\.\d+'
t_INTEGER = r'\d+'
t_DELIM = r','
t_QUOTE = r'"'

t_DASH = '-'
t_SLASH = '/'
t_ignore = '(\t| )'


def t_WORD(t):
    r"[A-Za-z&][A-Za-z&'.%]*[-]?"
    t.value = t.value.replace("'","")
    t.value = t.value.replace(".","")
    t.value = t.value.replace("-","")
    t.value = t.value.replace("&","_and_")
    t.value = t.value.replace("%","_PERCENTAGE")
    return t
    
def t_TEAM_STATE(t):
    r'\([A-Z]{2}\)'        
    t.value = ""
    return t
        
def t_NEWLINE(t):
    r'(\n)|(\r\n)'
    t.lexer.lineno +=1
    return t

    

# the tags state is to deal with the crap NCAA puts at the bottom of the files

states = (
    ('tags', 'exclusive'),
)   

def t_tags(t):
    r'<'
    t.lexer.begin('tags')

# the t_ignore for tags means it will skip over anything in between the '<>'
def t_tags_end(t):
    r'<>'
    t.lexer.begin('INITIAL') 

def t_tags_ANGLE_BRACKET_CLOSE(t):
    r'>'
    t.lexer.skip(1)

t_tags_ignore =  ' |\n|[A-Za-z+=.}{)(:"?;%&-]'

def t_tags_error(t):
    t.lexer.skip(1)

def t_error(t):
    print("Illegal character '{}' at line {}".format(
        t.value[0], t.lineno))
    t.lexer.skip(1)    


########################

    



def setUpLex(data):
    lexer = lex.lex()
    lexer.input(data.read())  
    


