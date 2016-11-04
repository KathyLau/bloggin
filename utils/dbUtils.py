import sqlite3
from pprint import pprint
conn = sqlite3.connect('tabular.db')
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
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title TEXT UNIQUE,
    subtitle TEXT,
    preContent TEXT,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    '''
    c.execute(q)

    q = '''
    CREATE TABLE extension (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    story_id INT NOT NULL,
    extContent TEXT,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    '''
    c.execute(q)


'''
USERINDB: tests if username exists in db file
> Input: STRING username to query for
> Output: True if username already in db, False otherwise
'''
def userInDB(username):
    q = "SELECT 1 FROM user WHERE username=\"%s\" LIMIT 1;" % username
    return True if c.execute(q).fetchone() else False


'''
LOGINAUTH: verifies login creds with db and returns corresponding int
> Input: STRING username, STRING password
> Output:
  > 0 if all ok
  > 1 if username empty
  > 2 if password empty
  > 3 if username doesn't exist
  > 4 if username DOES exist but wrong password
'''
def loginAuth(username, password):
    if not username: #username empty
        return 1
    if not password: #password empty
        return 2
    if userInDB(username):
        q = "SELECT 1 FROM user WHERE username=\"%s\" AND password=\"%s\" LIMIT 1;" % (username, password)
        correctPass = c.execute(q).fetchone()
        if correctPass:
            return 0
        return 4
    return 3


'''
REGISTERAUTH: verifies signup auth with db and returns corresponding int
> Input: STRING username, STRING password, STRING password_repeat
> Output:
  > 0 if all ok
  > 1 if username empty
  > 2 if pass or rpass empty
  > 3 if passwords don't match
  > 4 if username already exists
'''
def registerAuth(username, password, password_repeat):
    if not username:
        return 1
    if not password or not password_repeat:
        return 2
    if password != password_repeat:
        return 3
    q = "SELECT 1 FROM user WHERE username=\"%s\" LIMIT 1;" % username
    if userInDB(username):
        return 4
    return 0


'''
ADDUSER: Adds user to db
> Input: STRING username, STRING password_hashed
'''
def addUser(username, password_hashed):
    assert not userInDB(username), "*** TRIED TO ADD USER THAT ALREADY EXISTS ***"
    q = "INSERT INTO user(username, password) VALUES(\"%s\",\"%s\")" % (username, password_hashed)
    c.execute(q)
    conn.commit()

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

#TODO: check if user already commented on post

def tmp():
    q = "INSERT INTO user(username, password) VALUES(\"top\",\"kek\");"
    c.execute(q);
    q = "INSERT INTO user(username, password) VALUES(\"cop\",\"tech\");"
    c.execute(q);
    conn.commit()

    
def debug():
    #exists: [top: kek], [cop, tech]
    print "\nTESTING LOGIN..."
    print loginAuth("cop","lek") #should be 4
    print loginAuth("shop","kek") #should be 3
    print loginAuth("cop","") #should be 2
    print loginAuth("","tech") #should be 1
    print loginAuth("top","kek") #should be 0
    print loginAuth("cop","tech") #should be 0

    print "\nTESTING REGISTER..."
    print registerAuth("cop", "mop", "mop") #should be 4
    print registerAuth("top", "kek", "kek") #should be 4
    print registerAuth("shop", "lop", "mop") #should be 3
    print registerAuth("stop", "", "") #should be 2
    print registerAuth("stop", "abc", "") #should be 2
    print registerAuth("", "nop", "nop") #should be 1
    print registerAuth("pot", "kek", "kek") #should be 0
    print registerAuth("shop", "tech", "tech") #should be 0
    
    print "\nTESTING ADDUSER..."
    addUser("smol", "bloggos")
    addUser("bloggos", "smol")
    addUser("yawk", "kek")
    try:
        addUser("top", "asdf") #should throw error
    except:
        print "Threw user already found error!"
    print "Adding fetchUsers fxn later lmao"
    
    print "\nPRINTING TABLES..."
    printTable("user")
    printTable("story")
    printTable("extension")
    
if __name__ == "__main__":
    if 'user' not in getTables():
        setup()
        tmp()
    debug()

conn.close()
