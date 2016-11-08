'''
Recently added fxns in chrono order:
  ">" means priv use (iow: dwai)
  "!" means should implement in app.py
> setup, tmp, debug
! loginAuth, registerAuth
> isInDB (helper for auths)
> getTables, printTable (for debug)
! addUser (takes username and hashed pass)
! createStory
! getUserID (given username string)
! getContributedPosts
! getExtensionInfo (if using, pls read my doc for this)
! getStoryInfo (also this)
'''

import sqlite3
import dbUtils_helper as helper
from collections import defaultdict
from pprint import pprint
import os

conn = c = None #initialied in initConnection()


'''
initConnection: initiate connection w/ db
> Input: STRING path to db
>>> NOTE: must run before using any method here
'''
def initConnection(path):
    global conn, c
    conn = sqlite3.connect(path, check_same_thread=False)
    c = conn.cursor()
    helper.initConnection(path) #this is super messy, but necessary (im p sure)



'''
SETUP: sets up tables (if db is empty)
'''
def setup():
    if 'user' not in helper.getTables():
        q = '''
        CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(50),
        pfp TEXT
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
GETUSERID: get userID given username (presum to store in session)
> Input: STRING username
> Output: INT userID
'''
def getUserID(username):
    assert username.strip() and helper.isInDB( ("username",username) ) #username not blank and in DB
    q = "SELECT id FROM user WHERE username=? LIMIT 1;"
    return c.execute(q, (username,)).fetchone()[0] #should be user_id



'''
GETUSERNAME: get a user's username given ID
> Input: INT user_id
> Output: STRING username
'''
def getUsername(user_id):
    assert isinstance(user_id, (int, long)) and helper.isInDB( ("id", user_id) )
    q = "SELECT username FROM user WHERE id=? LIMIT 1;"
    return c.execute(q, (user_id,)).fetchone()[0]



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
    if helper.isInDB( ("username", username) ):
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
    if helper.isInDB( ("username", username) ):
        return 4
    return 0



'''
ADDUSER: Adds user to db
> Input: STRING username, STRING password (should be hashed by now!)
>>> NOTE: not returning anything b/c should have already verified everything in registerAuth()
'''
def addUser(username, password, pic):
    assert not helper.isInDB( ("username",username) ), "*** TRIED TO ADD USER THAT ALREADY EXISTS ***"
    q = "INSERT INTO user(username, password, pfp) VALUES(?,?,?)"
    c.execute(q, (username, password, pic))
    conn.commit()



'''
CREATESTORY: Adds newly created story to db
> Input
  > INT user_id (creator's user ID)
  > STRING title
  > STRING subtitle
  > STRING content (actual starting text of story)
> Output:
  > 0 if all ok
  > 1 if title empty
  > 2 if content empty
  > 3 if user already has story with same title
'''
def createStory(user_id, title, subtitle, content):
    assert isinstance(user_id, (int, long))
    if not title.strip():
        return 1
    if not content.strip():
        return 2
    if helper.isInDB( ("user_id",user_id), ("title",title), table="story"):
        return 3
    q = "INSERT INTO story(user_id, title, subtitle, content) VALUES(?,?,?,?)"
    c.execute(q, (user_id, title, subtitle, content))
    conn.commit()
    return 0



'''
EXTENDSTORY: add to another users' story instead of creating one
> Input: 
  > INT story_id (which story you're adding to)
  > INT user_id (YOUR user ID)
  > STRING content (what you're adding)
> Output:
  > 0 if all ok
  > 1 if content is empty
  > 2 if user already contributed to story
'''
def extendStory(user_id, story_id, content):
    #solely for easier debugging
    assert isinstance(user_id, (int, long)), "UserID not an int."
    assert isinstance(story_id, (int, long)), "StoryID not an int."
    assert helper.isInDB( ("id", user_id) ), "UserID not found in DB."
    assert helper.isInDB( ("id", story_id), table="story" ), "StoryID not found in DB!"
    if not content.strip():
        return 1

    #checking if user has either created or added this story
    if helper.isInDB(("story.user_id=%s OR extension.user_id"%user_id, user_id), \
              ("story.id=%s OR extension.story_id"%story_id, story_id), \
              table="story LEFT JOIN extension ON story.id = extension.story_id"):
        return 2
    q = "INSERT INTO extension(story_id, user_id, content) VALUES (?,?,?);"
    c.execute(q, (story_id, user_id, content))
    conn.commit()

    return 0



'''
GETEXTENSIONINFO: returns relevant info about a specific extension
> Input: INT extension_id
> Output: DEFAULTDICT (basically a dict) containing extension info
e.g. {
       'id': 1, 
       'user_id': 1,
       'author': "John Doe"
       'story_id': 1, 
       'content': "sample_extContent", 
       'create_ts': "yyyy-mm-dd hh:mm:ss"
     }
'''
def getExtensionInfo( extension_id ):
    assert helper.isInDB(("id", extension_id), table="extension"), "ExtensionID not found in DB!"
    q = "SELECT * FROM extension WHERE id=?;"
    extInfo_raw = c.execute(q, (extension_id,)).fetchone()
    extColumns = ("id", "user_id", "story_id", "content", "create_ts")

    #init values to list for cleaner code later
    extInfo = defaultdict(lambda:1)
    for i in xrange(len(extColumns)):
        extInfo[extColumns[i]] = extInfo_raw[i]

    extInfo["author"] = getUsername( extInfo["user_id"] )
    return extInfo



'''
GETSTORYINFO: returns relevant info about a specific story
> Input: INT story_id
> Output: DEFAULTDICT (basically a dict) containing story info
e.g. {
       'user_id': 1, 
       'id': 1, #this is the story id
       'title': "sample_title", 
       'subtitle': "sample_subtitle", 
       'content': "sample_content", #beginning of story
       'create_ts': "yyyy-mm-dd hh:mm:ss"
       'extensions': 
       [ <extension_id>, <extension_id>, ... ]
     }

>>> NOTE: Extensions are sorted in chronological order
>>> NOTE: Story without extensions will not have an "extensions" key
'''
def getStoryInfo( story_id ):
    assert helper.isInDB( ("id",story_id), table="story" ), "Story ID not found in DB!"
    
    #init values to list for cleaner code later
    storyInfo = defaultdict(list)

    q = '''
    SELECT story.id, story.user_id, story.title, story.subtitle, \
           story.content, story.create_ts, extension.id
    FROM story 
    LEFT JOIN extension
    ON story.id = extension.story_id 
    WHERE story.id = ?
    ORDER BY extension.create_ts;
    '''
    storyInfo_raw = c.execute(q, (story_id,))

    sampleRow = storyInfo_raw.fetchone() #for general story info
    storyColumns = ("id", "user_id", "title", "subtitle", "content", "create_ts")
    for i in xrange(len(storyColumns)):
        storyInfo[storyColumns[i]] = sampleRow[i]

    if sampleRow[ len(storyColumns) ]: # if story actually has extensions
        #add all the extension IDs to LIST storyInfo["extensions"]
        for row in c.execute(q, (story_id,)).fetchall():
            extension_id = row[ len(storyColumns) ] #row[6] should be extension_id column of joined table
            storyInfo["extensions"].append( extension_id ) 

    storyInfo["author"] = getUsername( storyInfo["user_id"] )
    return storyInfo



'''
GETCONTRIBUTEDSTORIES: returns info on all stories that user either created or added to, in *chronological order*
> Input: INT user_id
> Output: [LIST of {DICTS, each representing a post}]
e.g. [ <story_id>, <story_id>, ... ]
'''
def getContributedStories( user_id ):
    assert helper.isInDB( ("id",user_id) ), "UserID not found in DB!"
    q = '''
    SELECT DISTINCT story.id
    FROM story
    LEFT JOIN extension
    ON story.id = extension.story_id
    WHERE ? IN (story.user_id, extension.user_id)
    ORDER BY
    CASE WHEN extension.user_id IS NULL then story.create_ts ELSE extension.create_ts END;
    '''
    #CASE WHEN extension.user_id IS NULL then story.create_ts ELSE extension.create_ts END
    return [ user_id[0] for user_id in c.execute(q, (user_id,)).fetchall() ] #b/c fetchall puts the data in annoying tuple form


    
'''
GETNONCONTRIBUTEDSTORIES: returns info on all stories user has NOT created or added to, in *chronological order*
> Input: INT user_id
> Output: [LIST of {DICTS, each representing a post}]
e.g. [ <story_id>, <story_id>, ... ]
'''
def getNonContributedStories( user_id ):
    assert helper.isInDB( ("id",user_id) ), "UserID not found in DB!"
    
    q = '''
    SELECT DISTINCT story.id
    FROM story
    LEFT JOIN extension
    ON story.id = extension.story_id
    ORDER BY
    CASE WHEN extension.user_id IS NULL then story.create_ts ELSE extension.create_ts END;
    '''
    allPosts = [ story_id[0] for story_id in c.execute(q).fetchall() ] #b/c fetchall puts the data in annoying tuple form
    return list( filter((lambda x: x not in getContributedStories(user_id)), allPosts))



def debug():
    #init stuff
    q = "INSERT INTO user(username, password) VALUES(\"top\",\"kek\");"
    c.execute(q);
    q = "INSERT INTO user(username, password) VALUES(\"cop\",\"tech\");"
    c.execute(q);
    conn.commit()

    #using assert for less clutter in terminal
    #and sooner notice of error
    print "\nTESTING LOGIN..."
    try:
        assert loginAuth("cop","lek") == 4
        assert loginAuth("shop","kek") == 3
        assert loginAuth("cop","") == 2
        assert loginAuth("","tech") == 1
        assert loginAuth("top","kek") == 0
        assert loginAuth("cop","tech") == 0
        print "\tAll good!"
    except AssertionError, e:
        print "\t ERRORS!!!"
        raise

    print "\nTESTING REGISTER..."
    try:
        assert registerAuth("cop", "mop", "mop") == 4
        assert registerAuth("top", "kek", "kek") == 4
        assert registerAuth("shop", "lop", "mop") == 3
        assert registerAuth("stop", "", "") == 2
        assert registerAuth("stop", "abc", "") == 2
        assert registerAuth("", "nop", "nop") == 1
        assert registerAuth("pot", "kek", "kek") == 0
        assert registerAuth("shop", "tech", "tech") == 0
        print "\tAll good!"
    except AssertionError, e:
        print "\t ERRORS!!!"
        raise
    
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
        print "\tTHIS SHOULD HAVE THEN AN ERROR!"
        raise
    except:
        print "\tThrew user already found error! (intended)"

    print "\nTESTING GETUSERID..."
    try:
        assert getUserID("top") == 1
        assert getUserID("smol") == 3
        assert getUserID("bloggos") == 4
        assert getUserID("cop") == 2
        assert getUserID("yawk") == 5
        print "\tAll good!"
    except AssertionError, e:
        print "\to no didnt expect this one"
        raise
        

    print "\nTESTING CREATESTORY..."
    try:
        assert createStory(3, "  ", "w", "w") == 1
        assert createStory(3, "a", "b", "\t\n") == 2
        assert createStory(3, "title", "subtitle", "content") == 0
        assert createStory(3, "title", "b", "c") == 3
        assert createStory(getUserID("smol"), "smol_title", "smol", "smol") == 0
        assert createStory(getUserID("cop"), "no subtitle", "", "should work!") == 0
        print "\t* Stories just added to 'smol'(2) and 'cop'(1)"
    except AssertionError, e:
        print "\tmore errors asdfsasdf"
        raise

    print "\nTESTING EXTENDSTORY..."
    print "\t%d (should be 1)" % extendStory(getUserID("top"), 2, "\t  \n")
    print "\t%d (should be 2)" % extendStory(getUserID("smol"), 2, "smol wuz hear") #smol created story 1
    print "\t%d (should be 0)" % extendStory(getUserID("yawk"), 2, "yawk wuz hear")
    print "\t* 'yawk' just contributed to story 2 by smol"
    print "\t%d (should be 2)" % extendStory(getUserID("yawk"), 2, "yawk already hear") #yawk just added to story 2
    print "\t%d (should be 0)" % extendStory( getUserID("cop"), 2, "go away yawk")
    print "\t* 'cop' just contributed to story 2 by smol"

    print "\nTESTING GETSTORYINFO..."
    pprint( dict(getStoryInfo(1)) )
    pprint( dict(getStoryInfo(2)) )
    try:
        pprint( dict(getStoryInfo(-1)) )
        print "\tTHIS SHOULD NOT HAVE WORKED"
    except AssertionError, e:
        print "\tThrew an AssertionError (intended)"

    print "\nTESTING GETEXTENSIONINFO..."
    pprint( dict(getExtensionInfo(1)) )
    pprint( dict(getExtensionInfo(2)) )
    try:
        pprint( dict(getExtensionInfo(-1)) )
        print "\tTHIS SHOULD NOT HAVE WORKED"
    except AssertionError, e:
        print "* Threw an AssertionError (intended)"

    print "\nTESTING GETCONTRIBUTEDSTORIES..."
    print "\tbloggo's stories: " + str(getContributedStories( getUserID("bloggos") ))
    print "\tcop's stories: " + str(getContributedStories( getUserID("cop") ))
    print "\tsmol's stories: " + str(getContributedStories( getUserID("smol") ))
    try:
        getContributedStories(-1)
        print "\t*** THIS SHOULD NOT HAVE RUN ***"
    except AssertionError, e:
        print "* Threw an AssertionError (intended)"


    print "\nPRINTING USER TABLE..."
    helper.printTable("user")
    print "\nPRINTING STORY TABLE..."
    helper.printTable("story")
    print "\nPRINTING EXTENSION TABLE..."
    helper.printTable("extension")



if __name__ == "__main__":
    initConnection("data/tabular.db")
    setup()
    debug()
