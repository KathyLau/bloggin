from flask import Flask, render_template, request, redirect, url_for, session
import utils.dbUtils, hashlib 

app = Flask(__name__)

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("yourstories"))
    else:
        return redirect(url_for("login"))

@app.route("/yourstories")
def yourstories():
    posts = [{'title':'Dogs', 'subtitle':'An exploration into the canine psyche', 'author':'DanWasHere', 'content':'Indeed we all know dogs are rather friendly. But are they intelligent? Often the question is raised in academic circles if dogs could perhaps have more insight into what is going on around them than their slobbery smiling faces would indicate to the untrained eye'}, {'title':'Why Kelly', 'subtitle':"Damn it Kelly show up for school", "author":"DanWasHere", "content":"Dear Kelly, Show up for school, we miss you and your stuff is broken. Sincerely, Daniel"}]
    return render_template("multipleposts.html", postlist=posts, username=session["user"])
    
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
        if utils.dbUtils.loginAuth(user, pwd) == 0:
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
        if utils.dbUtils.registerAuth(user, pwd, confirm) == 0:
            hashObj = hashlib.sha1()
            hashObj.update(pwd)
            pwd = hashObj.hexdigest()
            utils.dbUtils.addUser(user, pwd)
            session["user"] = user
            return redirect(url_for("home"))
        return redirect(url_for("login"))


        
@app.route("/logout")
def logout():
    session.pop("user")
    return render_template("login.html")

@app.route("/new", methods=["GET", "POST"])
def create():
    if "user" in session:
        if request.method== "GET":
            return render_template("create.html", username=session["user"])
        else:
            post = request.form["post"]
            title = request.form["title"]
            sub = request.form["subtitle"]
            userID = session["user"]
            #SQL work
    else:
        return redirect(url_for("login"))

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" in session:
        if request.method== "GET":
            return render_template("add.html", username=session["user"])
        else:
            post = request.form["post"]
            title = request.form["title"]
            sub = request.form["subtitle"]
            userID = session["user"]
            #SQL work
    else:
        return redirect(url_for("login"))

        
if __name__=="__main__":
    app.debug = True
    app.secret_key = "dogs are qool"
    app.run()
