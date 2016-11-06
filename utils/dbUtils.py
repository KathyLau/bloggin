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
'''

import sqlite3
from dbUtils_helper import *

#!!! NOTE !!!: depending on where this is run, it will access different db files (one in /data/tabular.db and one in /utils/data/tabular.db
conn = sqlite3.connect('data/tabular.db', check_same_thread=False)

c = conn.cursor()


'''
GETUSERID: get userID given username (presum to store in session)
> Input: STRING username
> Output: INT userID
'''
def getUserID(username):
    assert username.strip() and isInDB( ("username",username) ) #username not blank and in DB
    q = "SELECT id, username FROM user WHERE username=? LIMIT 1;"
    return c.execute(q, (username,)).fetchone()[0] #should be user_id


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
    if isInDB( ("username", username) ):
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
    if isInDB( ("username", username) ):
        return 4
    return 0


'''
ADDUSER: Adds user to db
> Input: STRING username, STRING password (should be hashed by now!)
'''
def addUser(username, password):
    assert not isInDB( ("username",username) ), "*** TRIED TO ADD USER THAT ALREADY EXISTS ***"
    q = "INSERT INTO user(username, password) VALUES(?,?)"
    c.execute(q, (username, password))
    conn.commit()


'''
CREATESTORY: Adds newly created story to db
> Input
  > INT user_id (creator's user ID)
  > STRING title
  > STRING subtitle
  > STRING preContent (actual starting text of story)
> Output:
  > 0 if all ok
  > 1 if userID invalid (not int)
  > 2 if title empty
  > 3 if preContent empty
  > 4 if user already has story with same title
'''
def createStory(user_id, title, subtitle, preContent):
    if not isinstance(user_id, (int, long)):
        return 1
    if not title.strip():
        return 2
    if not preContent.strip():
        return 3
    q = "SELECT 1 FROM story WHERE user_id=? AND title=? LIMIT 1;"
    titleRepeated = c.execute(q, (user_id, title)).fetchone()
    if titleRepeated:
        return 4
    q = "INSERT INTO story(user_id, title, subtitle, preContent) VALUES(?,?,?,?)"
    c.execute(q, (user_id, title, subtitle, preContent))
    conn.commit()
    return 0


'''
EXTENDSTORY: add to another users' story instead of creating one
> Input: 
  > INT story_id (which story you're adding to)
  > INT user_id (YOUR user ID)
  > STRING extContent (what you're adding)
> Output:
  > 0 if all ok
  > 1 if user_id not an int
  > 2 if story_id not an int
  > 3 if user_id not found in user table
  > 4 if story_id not found in story table
  > 5 user already contributed to story
'''
def extendStory(user_id, story_id, extContent):
    #solely for easier debugging
    if not isinstance(user_id, (int, long)):
        return 1
    if not isinstance(story_id, (int, long)):
        return 2

    if not isInDB( ("id", user_id) ):
        return 3
    if not isInDB( ("id", story_id), table = "story" ):
        return 4

    #checking if user has either created or added this story
    if isInDB(("story.user_id=%s OR extension.user_id"%user_id, user_id), \
              ("story.id=%s OR extension.story_id"%story_id, story_id), \
              table="story LEFT JOIN extension ON story.id = extension.story_id"):
        return 5

    q = "INSERT INTO extension(story_id, user_id, extContent) VALUES (?,?,?);"
    c.execute(q, (story_id, user_id, extContent))
    conn.commit()
    return 0


'''
GETCONTRIBUTEDPOSTS: returns relevant info on all stories
that a user has either created or added to
> Input: INT user_id
> Output: [LIST of {DICTS representing posts}]
[
  {"title": "sample_title",
   "subtitle": "sample_subtitle",
   "creator
'''


def debug():
    #initial stuff
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
    except Exception, e:
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
    except Exception, e:
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
    except Exception, e:
        print "\to no didnt expect this one"
        raise
        

    print "\nTESTING CREATESTORY..."
    try:
        assert createStory("3", "a", "b", "c") == 1
        assert createStory(3, "  ", "w", "w") == 2
        assert createStory(3, "a", "b", "\t\n") == 3
        assert createStory(3, "title", "subtitle", "content") == 0
        assert createStory(3, "title", "b", "c") == 4
        assert createStory(getUserID("smol"), "smol_title", "smol", "smol") == 0
        assert createStory(getUserID("cop"), "no subtitle", "", "should work!") == 0
        print "\t* Stories added to 'smol'(2) and 'cop'(1) => All good!"
    except Exception, e:
        print "\tmore errors asdfsasdf"
        raise

    print "\nTESTING EXTENDSTORY..."
    print "\t%d (should be 1)" % extendStory("u",1,"c")
    print "\t%d (should be 2)" % extendStory(1,"s","c")
    print "\t%d (should be 3)" % extendStory(-1,2,"c")
    print "\t%d (should be 4)" % extendStory(3,-1,"c")
    print "\t%d (should be 5)" % extendStory(getUserID("smol"), 2, 1) #smol created story 1
    print "\t%d (should be 0)" % extendStory(getUserID("cop"), 2, "yawk wuz hear")
    print "\t%d (should be 5)" % extendStory(getUserID("cop"), 2, "yawk already hear") #yawk just added to story 2
    print "'yawk' contributed to story 2 by smol"


    print "\nPRINTING USERS..."
    printTable("user")
    print "\nPRINTING STORIES..."
    printTable("story")
    print "\nPRINTING EXTENSIONS..."
    printTable("extension")

    
if __name__ == "__main__":
    if 'user' not in getTables():
        setup()
    debug()
