from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date
import utils.dbUtils as dbUtils
import hashlib

app = Flask(__name__)
dbUtils.initConnection("data/tabular.db")
dbUtils.setup()

def getMaxPage():
    user = session["user"]
    userID = dbUtils.getUserID(user)
    contributed = dbUtils.getContributedStories(userID)
    numposts = len(contributed)
    return numposts/5 + 1

#root
@app.route("/")
def home():
    if "user" in session and session.get("user") != "admin":
        return redirect(url_for("yourstories", page=1))
    elif session.get("user") == "admin":
        return redirect(url_for("admin"))
    return redirect(url_for("login"))

#account pages
@app.route("/<username>")
def account(username):
    if assertionStuff() is not None:
        return assertionStuff()
    try:
        accountId = dbUtils.getUserID(username)
    except Exception:
        return redirect(url_for("home"))
    if username == "admin" and session["user"] != "admin":
        return redirect(url_for("home"))
    #user = session["user"]
    #userID = dbUtils.getUserID(user) #get user id
    contributed = dbUtils.getContributedStories(accountId)
    #contributed = dbUtils.getContributedStories(userID) #get stories
    numposts = len(contributed)
    contributed = contributed[::-1] #reverse first 5 chrono order
    posts = []
    for i in range( len(contributed) ):
        posts.append(dbUtils.getStoryInfo( contributed[i] ))
        posts[i]["create_ts"] = getFormattedDate( posts[i]["create_ts"] )
        for j in range( len(posts[i]["extensions"]) ): #expand extensions
            posts[i]["extensions"][j] = dbUtils.getExtensionInfo( posts[i]["extensions"][j] )
    accountPic = dbUtils.getUserPic(accountId)
    numUsers = dbUtils.getCountUsers()[0]
    return render_template("account.html", postlist=posts, username=session['user'], pic=accountPic, accountViewing=username, count=numUsers)

#admin page
@app.route("/admin", methods=['GET'])
def admin():
    if request.method=='GET' and session.get("user") == "admin":
        
        accountId = dbUtils.getUserID("admin")
        accountPic = dbUtils.getUserPic(accountId)
        
        censor = {"author":"SUPER ADMIN", "title": "censor", "subtitle": "replaces profile picture with ban hammer", "author_pic": accountPic, "content": ["username"]}
        rmuser = {"author":"SUPER ADMIN", "title": "removeuser", "subtitle": "removes user from database", "author_pic": accountPic, "content": ["username"]}
        viewData = {"author":"SUPER ADMIN", "title":"viewData", "subtitle": "view stuff from sql field", "author_pic": accountPic, "content": ["field", "table"]}
        posts = [censor, rmuser, viewData]
        return render_template("admin.html", accountViewing="admin", pic=accountPic, username="admin", postlist=posts)
    else:
        return redirect(url_for("home"))

@app.route("/admin/<command>", methods=['POST'])
def admincommand(command):
    accountId = dbUtils.getUserID("admin")
    accountPic = dbUtils.getUserPic(accountId)
    if request.method!="POST":
        return redirect(url_for("admin"))
    if command=="censor":
        username = request.form.get("username")
        try:
            dbUtils.censor(username)
        except TypeError:
            return redirect(url_for("admin"))
    if command=="removeuser":
        username = request.form.get("username")
        try:
            dbUtils.rmUser(username)
        except TypeError:
            return redirect(url_for("admin"))
    if command=="viewData":
        table = request.form.get("table")
        field = request.form.get("field")
        results = dbUtils.getDataFrom(table, field)
        #except Exception:
            #return redirect(url_for("admin"))
        postStr = ""
        numUsers = dbUtils.getCountUsers()[0]
        for result in results:
            postStr +=  result[0] + ", "
        contentpost = {"title": field + " from " + table, "subtitle":str(len(results))+" results", "author_pic": accountPic, "content": postStr}
        return render_template("account.html", username="admin", accountViewing="admin", postlist=[contentpost], count=numUsers)
        
    return redirect(url_for("admin"))
        
#search results
@app.route("/search", methods=['POST'])
def search():
    if assertionStuff() is not None:
        return assertionStuff()
    if request.method=="POST":
        query = request.form.get("query")
    else:
        return redirect(url_for("yourstories", page=1))
    contributed = dbUtils.getSearchResults(query)
    numposts = len(contributed)
    contributed = contributed[::-1] #reverse first 5 chrono order
    posts = []
    for i in range( len(contributed) ):
        posts.append(dbUtils.getStoryInfo( contributed[i][0]))
        posts[i]["create_ts"] = getFormattedDate( posts[i]["create_ts"] )
        for j in range( len(posts[i]["extensions"]) ): #expand extensions
            posts[i]["extensions"][j] = dbUtils.getExtensionInfo( posts[i]["extensions"][j] )
    maxposts = len(posts)/5 + 1
    numUsers = dbUtils.getCountUsers()[0]
    return render_template("multipleposts.html", count=numUsers, postlist=posts, username=session['user'], page=1, maxpage=maxposts)


#lands on this page after you click continue reading
@app.route("/<username>/<postID>", methods=["GET","POST"])
def viewPost(username, postID):
    
    if assertionStuff() is not None:
        return assertionStuff()
    userID = dbUtils.getUserID(session['user'])

    extra = ""
    
    if request.method == "POST":
        content = request.form.get("extension")

        if dbUtils.extendStory( userID, int(postID), content ) != 0:
            extra = "dun goofed"

    story = dbUtils.getStoryInfo(postID)
    extensions = [ dbUtils.getExtensionInfo(extID) for extID in story['extensions'] ]
    story["create_ts"] = getFormattedDate( story["create_ts"])

    hasContributed = int(postID) in dbUtils.getContributedStories(userID) or session["user"]=="admin"
    numUsers = dbUtils.getCountUsers()[0]
    return render_template("single.html", post=story, count=numUsers, extensions=extensions, username=session['user'], extra=extra, hasContributed=hasContributed)


@app.route("/find/<int:page>")
def find(page):
    if assertionStuff() is not None:
        return assertionStuff()
    user = session["user"]
    userID = dbUtils.getUserID(user)
    notContributed = dbUtils.getNonContributedStories(userID)
    numposts = len(notContributed)
    if page >=0 and page <= numposts / 5 + 1:
        notContributed = notContributed[::-1][5 * (page-1):5 * page] #reverse first 5 chrono order
    else:
        return redirect(url_for("find", page=1))
    posts = []
    for i in range( len(notContributed) ):
        posts.append(dbUtils.getStoryInfo( notContributed[i] ))
        posts[i]["create_ts"] = getFormattedDate( posts[i]["create_ts"] )
        for j in range( len(posts[i]["extensions"]) ): #expand extensions
            posts[i]["extensions"][j] = dbUtils.getExtensionInfo( posts[i]["extensions"][j] )
    numUsers = dbUtils.getCountUsers()[0]
    return render_template("multipleposts.html", count=numUsers, postlist=posts, username=user, explore=1, page = page, maxpage=numposts/5+1)


#view stories you created or contributed to
# / page number starts on 1, loads 5 stories per page
@app.route("/yourstories/<int:page>")
def yourstories(page):
    if assertionStuff() is not None:
        return assertionStuff()
    user = session["user"]
    userID = dbUtils.getUserID(user) #get user id
    contributed = dbUtils.getContributedStories(userID) #get stories
    numposts = len(contributed)
    if page >= 1 and page <= numposts / 5 + 1:
        contributed = contributed[::-1][5 * (page-1):5 * page] #reverse first 5 chrono order
    else:
        return redirect(url_for("yourstories", page=1))
    posts = []
    for i in range( len(contributed) ):
        posts.append(dbUtils.getStoryInfo( contributed[i] ))
        posts[i]["create_ts"] = getFormattedDate( posts[i]["create_ts"] )
        for j in range( len(posts[i]["extensions"]) ): #expand extensions
            posts[i]["extensions"][j] = dbUtils.getExtensionInfo( posts[i]["extensions"][j] )

    numUsers = dbUtils.getCountUsers()[0]
    return render_template("multipleposts.html", count=numUsers, postlist=posts[:5], username=session['user'], page = page, maxpage=numposts/5+1)


#login for regusted users
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        user = request.form["user"]
        pwd = request.form["pass"]
        #check if hashed password is the same
        hashObj = hashlib.sha1()
        hashObj.update(pwd)
        pwd = hashObj.hexdigest()
        #fxn to verify w SQL
        #if true: add session and redirect to home page
        if dbUtils.loginAuth(user, pwd) == 0:
            #else return login page
            session["user"] = user
            return redirect(url_for("home"))
        else:
            return render_template("login.html", extra = "LOGIN INCORRECT")


#register an account
@app.route("/register", methods=["GET", "POST"])
def reg():
    if request.method=="GET":
        return render_template("register.html")
    #else return reg page
    else:
        user = request.form["user"]
        pwd = request.form["pass"]
        confirm = request.form["confirm"]
        pic = request.form["pic"]
        if dbUtils.registerAuth(user, pwd, confirm) == 0:
            #hash the password
            hashObj = hashlib.sha1()
            hashObj.update(pwd)
            pwd = hashObj.hexdigest()
            #add it to the SQL
            dbUtils.addUser(user, pwd, pic)
            session["user"] = user #store session
            return redirect(url_for("home"))
        return render_template("register.html")


#Logout - pop user out of session bye
@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
    return redirect("/")

#create a new story page
@app.route("/new", methods=["GET", "POST"])
def create():
    if assertionStuff() is not None:
        return assertionStuff()
    if request.method== "GET":
        numUsers = dbUtils.getCountUsers()[0]
        return render_template("create.html", count=numUsers, username=session["user"])
    else:
        #getting data from form
        post = request.form["post"]
        title = request.form["title"]
        sub = request.form["subtitle"]
        user = session["user"]
        userID = dbUtils.getUserID(user)
        #SQL work
        dbUtils.createStory(userID, title, sub, post)
        numUsers = dbUtils.getCountUsers()[0]
        return redirect(url_for("yourstories", count=numUsers, page=1, maxpage = getMaxPage() ))


#format date and timestamp from timestamp in sql table
def getFormattedDate( timestamp ):
    # split the date like 2016-11-07 in the table
    dateList = timestamp[:timestamp.find(" ")].split("-")
    dateString = date(
        day = int(dateList[2]),
        month = int(dateList[1]),
        year = int(dateList[0]),
    ).strftime('%B %d, %Y')
    # timeString is the exact time like 9:07:43
    timeString = timestamp[timestamp.find(" ")+1:][:-3]
    return "%s\n%s" % (dateString, timeString)


#to check is user is logged in
def assertionStuff():
    if "user" not in session:
        #if not return to root page
        return redirect( "/" )
    try:
        #get user id
        dbUtils.getUserID( session["user"] )
    except AssertionError, e:
        return redirect( "/logout" )


if __name__=="__main__":
    app.debug = True
    app.secret_key = "dogs are qool"
    app.run()
