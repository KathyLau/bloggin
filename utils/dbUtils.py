import sqlite3
conn = sqlite3.connect('tabular.db')
c = conn.cursor()

def setup():
    q = '''
    CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)
    )
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
    )
    '''
    c.execute(q)

    q = '''
    CREATE TABLE extension (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    story_id INT NOT NULL,
    extContent TEXT,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    )
    '''
    c.execute(q)


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
    q = "SELECT 1 FROM user WHERE username=\"%s\" LIMIT 1;" % username
    userExists = c.execute(q).fetchone()
    if userExists:
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
    userExists = c.execute(q).fetchone()
    if userExists:
        return 4
    return 0


def tmp():
    q = "INSERT INTO user(username, password) VALUES(\"top\",\"kek\")"
    c.execute(q);
    q = "INSERT INTO user(username, password) VALUES(\"cop\",\"tech\")"
    c.execute(q);


def tables():
    if c != None:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        stringtable = []
        for table in c.fetchall():
            stringtable.append(str(table[0]))
            return stringtable
        
def debug():
    print loginAuth("cop","lek") #should be 4
    print loginAuth("shop","kek") #should be 3
    print loginAuth("cop","") #should be 2
    print loginAuth("","tech") #should be 1
    print loginAuth("top","kek") #should be 0
    print loginAuth("cop","tech") #should be 0

demtables = tables()
if "user" not in demtables and "story" not in demtables and "extension" not in demtables:
    setup()
debug()
conn.commit()
conn.close()
