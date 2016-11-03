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
LOGIN: verifies login auth with db and returns corresponding int
> Input: STRING username, STRING password
> Output:
  > 0 if all ok
  > 1 if username doesn't exist
  > 2 if username DOES exist but wrong password
'''
def login(username, password):
    q = "SELECT 1 FROM user WHERE username=\"%s\" LIMIT 1;" % username
    userExists = c.execute(q).fetchone()

    if userExists:
        q = "SELECT 1 FROM user WHERE username=\"%s\" AND password=\"%s\" LIMIT 1;" % (username, password)
        correctPass = c.execute(q).fetchone()

        if correctPass:
            return 0
        return 2
    return 1


def tmp():
    q = "INSERT INTO user(username, password) VALUES(\"top\",\"kek\")"
    c.execute(q);
    q = "INSERT INTO user(username, password) VALUES(\"cop\",\"tech\")"
    c.execute(q);


def debug():
    print login("cop","lek") #should be 2
    print login("shop","kek") #should be 1
    print login("top","kek") #should be 0
    print login("cop","tech") #should be 0

debug()
conn.commit()
conn.close()
