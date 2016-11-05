'''
Recently added fxns in chrono order:
  ">" means priv use (iow: dwai)
  "!" means should implement in app.py
> setup, tmp, debug
! loginAuth, registerAuth
> userInDB (helper for auths)
> getTables, printTable (for debug)
! addUser (takes username and hashed pass)
! addStory
! getUserID (given username string)
> userInDB (takes EITHER username or userID) 
'''

import sqlite3
from pprint import pprint
print __name__
#!!! NOTE !!!: depending on where this is run, it will access different db files (one in /data/tabular.db and one in /utils/data/tabular.db
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
    preContent TEXT,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    '''
    c.execute(q)

    q = '''
    CREATE TABLE extension (
    id INTEGER PRIMARY KEY,
    user_id INT NOT NULL,
    story_id INT NOT NULL,
    extContent TEXT,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    );
    '''
    c.execute(q)


'''
USERINDB: tests if userID/username exists in db file
> Input: INT userID *OR* STRING username to query for existance
> Output: True if user already in db, False otherwise
'''
def userInDB(user):
    if isinstance(user, (int, long)): #was given ID
        q = "SELECT 1 FROM user WHERE id=? LIMIT 1;"
    else:
        assert isinstance(user, (str, unicode)), "*** user was invalid type: %s ***" % type(user)
        q = "SELECT 1 FROM user WHERE username=? LIMIT 1;"
    return True if c.execute(q, (user,)).fetchone() else False


'''
GETUSERID: get userID given username (presum to store in session)
> Input: STRING username
> Output: INT userID
'''
def getUserID(username):
    assert username.strip() and userInDB(username) #username not blank and in DB
    q = "SELECT id, username FROM user WHERE username=? LIMIT 1;"
    return c.execute(q, (username,)).fetchone()[0] #should be userID


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
    if not username.strip(): #username empty
        return 1
    if not password.strip(): #password empty
        return 2
    if userInDB( username ):
        q = "SELECT 1 FROM user WHERE username=? AND password=? LIMIT 1;"
        correctPass = c.execute(q, (username, password)).fetchone()
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
    if not username.strip():
        return 1
    if not password.strip() or not password_repeat.strip():
        return 2
    if password != password_repeat:
        return 3
    if userInDB( username ):
        return 4
    return 0


'''
ADDUSER: Adds user to db
> Input: STRING username, STRING password_hashed
'''
def addUser(username, password_hashed):
    assert not userInDB(username), "*** TRIED TO ADD USER THAT ALREADY EXISTS ***"
    q = "INSERT INTO user(username, password) VALUES(?,?)"
    c.execute(q, (username, password_hashed))
    conn.commit()


'''
ADDSTORY: Adds newly created story to db
> Input: INT userID, STRING title, STRING subtitle, STRING preContent
> Output:
  > 0 if all ok
  > 1 if userID invalid (not int)
  > 2 if title empty
  > 3 if preContent empty
  > 4 if user already has story with same title
'''
def addStory(userID, title, subtitle, preContent):
    if not isinstance(userID, (int, long)):
        return 1
    if not title.strip():
        return 2
    if not preContent.strip():
        return 3
    q = "SELECT 1 FROM story WHERE user_id=? AND title=? LIMIT 1;"
    titleRepeated = c.execute(q, (userID, title)).fetchone()
    if titleRepeated:
        return 4
    q = "INSERT INTO story(user_id, title, subtitle, preContent) VALUES(?,?,?,?)"
    c.execute(q, (userID, title, subtitle, preContent))
    conn.commit()
    return 0


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
    print "\t%d (should be 4)" % loginAuth("cop","lek")
    print "\t%d (should be 3)" % loginAuth("shop","kek")
    print "\t%d (should be 2)" % loginAuth("cop","")
    print "\t%d (should be 1)" % loginAuth("","tech")
    print "\t%d (should be 0)" % loginAuth("top","kek")
    print "\t%d (should be 0)" % loginAuth("cop","tech")

    print "\nTESTING REGISTER..."
    print "\t%d (should be 4)" % registerAuth("cop", "mop", "mop")
    print "\t%d (should be 4)" % registerAuth("top", "kek", "kek")
    print "\t%d (should be 3)" % registerAuth("shop", "lop", "mop")
    print "\t%d (should be 2)" % registerAuth("stop", "", "")
    print "\t%d (should be 2)" % registerAuth("stop", "abc", "")
    print "\t%d (should be 1)" % registerAuth("", "nop", "nop")
    print "\t%d (should be 0)" % registerAuth("pot", "kek", "kek")
    print "\t%d (should be 0)" % registerAuth("shop", "tech", "tech")
    
    print "\nTESTING ADDUSER..."
    try:
        addUser("smol", "bloggos")
        addUser("bloggos", "smol")
        addUser("yawk", "kek")
        print "\t* Users 'smol', 'bloggos', and 'yawk' added"
    except:
        print "\t*** ADDUSER ERROR ***"
        raise
    try:
        addUser("top", "asdf") #should throw error
    except:
        print "\tThrew user already found error! (intended)"

    print "\nTESTING GETUSERID..."
    print "\t%d (should be 1)" % getUserID("top")
    print "\t%d (should be 3)" % getUserID("smol")
    print "\t%d (should be 4)" % getUserID("bloggos")
    print "\t%d (should be 2)" % getUserID("cop")
    print "\t%d (should be 5)" % getUserID("yawk")

    print "\nTESTING ADDSTORY..."
    print "\t%d (should be 1)" % addStory("3", "a", "b", "c")
    print "\t%d (should be 2)" % addStory(3, "  ", "w", "w")
    print "\t%d (should be 3)" % addStory(3, "a", "b", "\t\n")
    print "\t%d (should be 0)" % addStory(3, "title", "subtitle", "content")
    print "\t%d (should be 4)" % addStory(3, "title", "b", "c")
    print "\t%d (should be 0)" % addStory(getUserID("cop"), "no subtitle", "", "should work!")
    print "\t* Stories added to 'smol' and 'cop'"

    print "\nPRINTING USERS..."
    printTable("user")

    print "\nPRINTING STORIES..."
    printTable("story")

    print "\nPRINTING EXTENSIONS..."
    printTable("extension")

    
if __name__ == "__main__":
    if 'user' not in getTables():
        setup()
        tmp()
    debug()
