from flask import Flask, render_template, request, redirect, url_for
import util.dbUtils 

app = Flask(__name__)

@app.route("/")
def home():

    #So i know i'm doing front-end but I just made an example of how the jinja template parses articles at the moment. This is my idea for now
    posts = [{'title':'Dogs', 'subtitle':'An exploration into the canine psyche', 'author':'DanWasHere', 'content':'Indeed we all know dogs are rather friendly. But are they intelligent? Often the question is raised in academic circles if dogs could perhaps have more insight into what is going on around them than their slobbery smiling faces would indicate to the untrained eye'}]
    return render_template("index.html", postlist=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        user = request.form["user"]
        pwd = request.form["pass"]
        #fxn to verify w SQL
        #if true: add session and redirect to home page
        if util.dbUtils.loginAuth == True:
        #else return login page
            session["user"] = user
            redirect(url_for("home"))
        else:
            return render_template("login.html", extra = "LOGIN INCORRECT")

@app.route("/register", methods=["GET", "POST"])
def reg():
    if request.method=="GET":
        return render_template("register.html")
    else:
        user = request.form["user"]
        pwd = request.form["pass"]
        #fxn to check if username !exists in SQL
        #if true: add the user to SQL, redirect to login
        redirect(url_for("login"))
        
@app.route("/logout")
def logout():
    session.pop["user"]
    return render_template("index.html")

if __name__=="__main__":
    app.debug = True
    app.run()
