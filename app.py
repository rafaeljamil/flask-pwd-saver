from flask import Flask, render_template, request, redirect, url_for, make_response, session
import secrets
import app_commands as app_cmd


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
        username = request.form["username"]
        password = request.form["password"]
        user_login = app_cmd.user_login(username, password)
        print(user_login)
        if user_login["user"] == -1:
            return "<h1>Usuário não encontrado</h1>"
        else:
            if user_login["data"] == -1:
                return "<h1> Senha Inválida </h1>"
            else:
                user_info = [v for v in user_login["data"].values()]
                session["user_id"] = user_info[0]
                session["username"] = user_info[1]
                return redirect(url_for("home"))

@app.route("/registrar", methods=["GET","POST"])
def registrar():
    if request.method == "POST":
        #Cria novo usuário
        username = request.form["username"]
        password = request.form["password"]
        confirm_pwd = request.form["password1"]
        if confirm_pwd == password:
            new_user = app_cmd.new_user(username, password)
            if new_user["create_user"] == 0 and new_user["create_token"] == 0:
                return redirect(url_for("login"))
        else:
            return "<h3> Usuário não criado. Tente novamente mais tarde </h3>"
    else:
        #Mostra página de registro
        return render_template("registrar.html")

@app.route("/<username>/buscar", methods=["GET","POST"])
def buscar(username):
    #Busca por nome EXATO do serviço
    #TODO: Buscar por parte do nome do serviço
    if request.method == "POST":
        data = [session["user_id"], request.form["busca"]] #Esperando organizar lógica do login
        busca = app_cmd.find_entry_by_name(data)
        ret_busca = busca
        return render_template("form_busca.html", busca=ret_busca, user=username) #Retorna None se não existir a busca no banco, ou a senha descriptografada
    else:
#        return render_template("form_busca.html")
        return render_template("form_busca.html", busca=0, user=username) #Valor de busca no GET

@app.route("/<username>/criar", methods=["GET","POST"])
def criar(username):
    #Cria nova entrada de serviço
    if request.method == "POST":
        data = [session["user_id"], session["username"], request.form["service"], request.form["password"], request.form["usr_pwd"]]
        entry = app_cmd.create_entry(data)
        msg = "Novo serviço criado com sucesso" if entry == 0 else "Erro ao criar serviço"
        return render_template("form_novo.html", message = msg, user=username)
    else:
        return render_template("form_novo.html", message = "", user=username)

@app.route("/<username>/editar", methods=["GET","POST"])
def editar(username):
    if request.method == "POST":
        data = [session["user_id"], request.form["busca"]]
        busca = app_cmd.check_entry(data)
        if busca == None:
            msg = "Serviço não encontrado."
            return render_template("form_editar.html", message = msg, user=username)
        else:
            msg = "Serviço encontrado."
            return render_template("form_editar.html", message = msg, user=username)
    else:
        return render_template("form_editar.html", message = "", user=username)

@app.route("/<username>/editar/<service>", methods=["GET","POST"])
def editar_servico(username, service):
    pass
