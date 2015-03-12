import ConfigParser



config_file="stats.ini"
config = ConfigParser.SafeConfigParser()
config.read(config_file)


def getSQLDB():
    return config.get('SQL', 'db')
    

def getSQLUserName():
    return config.get('SQL', 'username')
    
def getSQLHost():
    return config.get('SQL', 'host')
    
    
    
def setSQLDB(db):
    raise NotImplementedError
    
def setSQLUserName(name):
    raise NotImplementedError
    
def setSQLHost(host):
    raise NotImplementedError





