import sqllite3
c = sqlite3.connect('../data/tabular.db')

def setup():
    q = '''
    CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50),
    )
    '''
    
    q = '''
    CREATE TABLE story (
    id INT NOT NULL AUTO_INCREMENT,
    int user_id int not null,
    title TEXT,
    subtitle TEXT,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
    )

    '''
    c.execute(q)





    
c.close();
