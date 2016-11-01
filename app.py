from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        user = request.form["user"]
        pwd = request.form["pwd"]
        #fxn to verify w SQL
        #if true: add session and redirect to home page
        #else return login page
        

@app.route("/register", methods=["GET", "POST"])
def reg():
    if request.method=="GET":
        return render_template("register.html")
    else:
        user = request.form["user"]
        pwd = request.form["pwd"]
        #fxn to check if username !exists in SQL
        #if true: add the user to SQL, redirect to login
        #else: refresh
        
@app.route("/logout")
def logout():
    session.pop["user"]
    return render_template("index.html")

if __name__=="__main__":
    app.debug = True
    app.run()
