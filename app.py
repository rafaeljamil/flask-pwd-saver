from flask import Flask, render_template, g, request, redirect, url_for, make_response, session
import secrets
import cli_app as funcs


app = Flask(__name__)

app.secret_key = secrets.token_hex()

@app.route("/")
@app.route("/home", methods=["GET"])
def home():
    # Usando sessão
    if not "username" in session:
        return redirect(url_for("login"))
    user = session["username"]
    #user = "USER TESTE"    
    return render_template("home.html", user=user)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        session["username"] = request.form["username"]
    return redirect(url_for("home"))

@app.route("/buscar", methods=["GET","POST"])
def buscar():
    #if request.method == "GET":
    if request.method == "POST":
        busca = funcs.
        ret_busca = [1,2,"busca", "abc123", request.form["busca"]]
        return render_template("form_busca.html", busca=ret_busca)
    else:
        return render_template("form_busca.html", busca=0)
