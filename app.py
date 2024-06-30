from flask import Flask, render_template, g, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    user = request.cookie.get("username")
    return render_template("home.html", user)

@app.route("/login", methods=["GET","POST"])
def login():
    res: list = []
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        res.append(request.form["username"])
        res.append(request.form["password"])
        request.cookie.set("username", request.form["username"])
        print(res)
    return redirect(url_for("home"))
