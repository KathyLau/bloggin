import sqlite3
c = sqlite3.connect('tabular.db')

def setup():
    q = '''
    CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
    )
    '''
    c.execute(q)

    q = '''
    CREATE TABLE story (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title TEXT,
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


setup()

c.close();
