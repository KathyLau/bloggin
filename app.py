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

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("yourstories", page=1, maxpage = getMaxPage()))
    return redirect(url_for("login"))


    
@app.route("/<username>/<postID>", methods=["GET","POST"])
def viewPost(username, postID):
    if assertionStuff() is not None:
        return assertionStuff()
    userID = dbUtils.getUserID(username)
    
    extra = ""
    if request.method == "POST":
        content = request.form.get("extension")

        if dbUtils.extendStory( userID, int(postID), content ) != 0:
            extra = "dun goofed"
            
    story = dbUtils.getStoryInfo(postID)
    extensions = [ dbUtils.getExtensionInfo(extID) for extID in story['extensions'] ]
    story["create_ts"] = getFormattedDate( story["create_ts"])
    
    hasContributed = int(postID) in dbUtils.getContributedStories(userID)
    return render_template("single.html", post=story, extensions=extensions, username=session['user'], extra=extra, hasContributed=hasContributed)
            


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
    
    return render_template("multipleposts.html", postlist=posts, username=user, explore=1, page = page, maxpage=numposts/5+1)


@app.route("/yourstories/<int:page>")
def yourstories(page):
    if assertionStuff() is not None:
        return assertionStuff()
    user = session["user"]
    userID = dbUtils.getUserID(user)
    contributed = dbUtils.getContributedStories(userID)
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

    return render_template("multipleposts.html", postlist=posts[:5], username=session['user'], page = page, maxpage=numposts/5+1)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        user = request.form["user"]
        pwd = request.form["pass"]
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



@app.route("/register", methods=["GET", "POST"])
def reg():
    if request.method=="GET":
        return render_template("register.html")
    #else return reg page
    else:
        user = request.form["user"]
        pwd = request.form["pass"]
        confirm = request.form["confirm"]
        if dbUtils.registerAuth(user, pwd, confirm) == 0:
            hashObj = hashlib.sha1()
            hashObj.update(pwd)
            pwd = hashObj.hexdigest()
            dbUtils.addUser(user, pwd)
            session["user"] = user
            return redirect(url_for("home"))
        return redirect(url_for("login"))


        
@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def create():
    if assertionStuff() is not None:
        return assertionStuff()
    if request.method== "GET":
        return render_template("create.html", username=session["user"])
    else:
        post = request.form["post"]
        title = request.form["title"]
        sub = request.form["subtitle"]
        user = session["user"]
        userID = dbUtils.getUserID(user)
        #SQL work
        dbUtils.createStory(userID, title, sub, post)
        return redirect(url_for("yourstories", page=1, maxpage = getMaxPage() ))
        

def getFormattedDate( timestamp ):
    dateList = timestamp[:timestamp.find(" ")].split("-")
    dateString = date(
        day = int(dateList[2]), 
        month = int(dateList[1]), 
        year = int(dateList[0]),
    ).strftime('%B %d, %Y')
    timeString = timestamp[timestamp.find(" ")+1:][:-3]
    return "%s\n%s" % (dateString, timeString)


def assertionStuff():
    if "user" not in session:
        return redirect( "/" )
    try:
        dbUtils.getUserID( session["user"] )
    except AssertionError, e:
        return redirect( "/logout" )


if __name__=="__main__":
    app.debug = True
    app.secret_key = "dogs are qool"
    app.run()

