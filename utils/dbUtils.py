import sqllite3
c = sqlite3.connect('../data/tabular.db')

def setup():
    q = '''
    CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT;
    username VARCHAR(50),
    password VARCHAR(50),
    )
    '''
    c.execute(q)



c.close();
