import sqlite3
from pprint import pprint

#I verified multiple conns are supported by sqlite3 :)
conn = sqlite3.connect('data/tabular.db', check_same_thread=False)
c = conn.cursor()


def setup():
    q = '''
    CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)
    );
    '''
    c.execute(q)

    q = '''
    CREATE TABLE story (
    id INTEGER PRIMARY KEY,
    user_id INT NOT NULL,
    title TEXT,
    subtitle TEXT,
    content TEXT,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    '''
    c.execute(q)

    q = '''
    CREATE TABLE extension (
    id INTEGER PRIMARY KEY,
    user_id INT NOT NULL,
    story_id INT NOT NULL,
    content TEXT,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    '''
    c.execute(q)
    conn.commit()


'''
ISINDB: tests if row exists in db file
> Input: 
  > [keyword] table = STRING
  > *[var] TUPLE (<column>, <value>)
> Output: True if user already in db, False otherwise
'''
#readability kinda went out the window for this one
#throws error if column name doesn't exist
def isInDB(*columns,**table):return True if c.execute("SELECT 1 FROM %s WHERE %s LIMIT 1;"%(table["table"]if table else"user",reduce((lambda c1,c2:"(%s) AND (%s)"%("%s=\"%s\""%(columns[0][0],columns[0][1])if isinstance(c1,tuple)else c1,"%s=\"%s\""%(c2[0],c2[1]))),columns)if len(columns)-1 else"%s=\"%s\""%(columns[0][0],columns[0][1]))).fetchone() else False

# For easier reading: ...
'''
def isInDB(*columns,**table):

    table = table["table"] if table else "user"

    if len(columns)-1:
        g = reduce( (lambda c1,c2:"(%s) AND (%s)"%("%s=\"%s\""%(columns[0][0],columns[0][1])if isinstance(c1,tuple)else c1,"%s=\"%s\""%(c2[0],c2[1]))),columns)
    else:
        g = "%s=\"%s\"" % (columns[0][0], columns[0][1])

    q = "SELECT 1 FROM %s WHERE %s LIMIT 1;" % (table, g)
    print q
    
    if c.execute(q).fetchone():
        return True
    return False
'''


'''
GETTABLES: temp fxn to check if tables created already
> Output: list of table names IF cursor exists, None otherwise
'''
def getTables():
    if c != None:
        q = "SELECT name FROM sqlite_master WHERE type='table';"
        c.execute(q)
        list_tableName = map((lambda table: str(table[0])), c.fetchall())
        return list_tableName
    return None


'''
PRINTTABLE: prints out table in DB in human-readable format
> Input: STRING tableName
'''
def printTable(tableName):
    q = "SELECT * FROM %s;" % tableName
    tableData = c.execute(q).fetchall()
    pprint(tableData)

