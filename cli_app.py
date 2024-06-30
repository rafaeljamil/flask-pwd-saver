# CLI para testes e configurações.
import fernet_commands as fc
import database_commands as db
import os
import time

# Organizando Funções

# Limpar tela do terminal
def clear_screen() -> None:
    if os.uname().sysname == "Linux":
        os.system("clear")
    else:
        os.system("cls")

def new_user():
    clear_screen()
    user = input("Escolha um nome de usuário: ")
    password = input("Escolha uma senha: ")
    print(f"Você escolheu {user} como usuário e {password} como senha.")    
    if input("Você confirma os dados acima? ").lower() in ["yes", "y", "sim", "s"]:
        user_key = fc.create_key()
        enc_pwd = fc.enc_msg(user_key, password)
        user_info = [user, enc_pwd]
        db.insert_user(user_info)
        print("Usuário criado.")
        user = db.query_database("users", "username", user).fetchone()
        user_id = user['id']        
        db.insert_token([user_id, user_key])
        print("Token salvo.")
    else:
        print("Dados não confirmados. Cancelando ação.")

# fazer login do usuário
def user_login() -> list:
    # Pega input de usuário e senha, checa o banco de dados pra ver se está correto e retorna uma lista com informações do usuário
    username = input("Usuário -> ")
    password = input("Senha -> ")
    db_user = db.query_database("users", "username", username).fetchone()
    if db_user == None:
        print("Usuário não encontrado.")
        time.sleep(3)
    else:
        db_fernet = db.query_database("tokens", "user_id", db_user['id']).fetchone()
        dec_pwd = fc.dec_msg(db_fernet['token'], db_user['password'])
        print(dec_pwd)
        if password == dec_pwd:
            user_info = [db_user['id'], db_user['username']]
            return user_info
        else:
            print("Senha inválida...")
            time.sleep(3)
            return []
    #db_user.close()
    #db_fernet.close()
    

# Nova entrada de serviço, site ou app e a respectiva senha criptografada
def create_entry(username: str, user_id: int):
    service = input("Nome do serviço, site ou app: ")
    svc_pwd = input("Senha do serviço, site ou app: ")
    usr_pwd = input("Confirme a senha de usuário: ")
    db_user = db.query_database("users", "username", username).fetchone()
    db_fernet = db.query_database("tokens", "user_id", user_id).fetchone()
    dec_pwd = fc.dec_msg(db_fernet["token"], db_user["password"])
    if usr_pwd == dec_pwd:
        # Ao confirmar com senha, o processo de criptografia começa
        enc_svc_pwd = fc.enc_msg(db_fernet['token'], svc_pwd)
        data = [user_id, service, enc_svc_pwd]
        db.insert_service(data)
        print("Nova entrada salva com sucesso.")
        time.sleep(3)
    else:
        print("Senha inválida...")
        time.sleep(3)
    #db_user.close()
    #db_fernet.close()


# Buscar serviço, site ou app, decripta a senha salva no banco e mostra pro usuário
def find_entry_by_name(user_id: int, entry: str):
    # buscando todas as chaves do usuário logado pra encontrar o serviço que ele quer. Se buscar por serviço pode vazar dados de outros usuários.
    db_script = f"SELECT * FROM services WHERE user_id = {user_id} AND service_name = '{entry}'"    
    query = db.query_database_script(db_script).fetchone()
    if query == None:
        print("Serviço, site ou app não encontrado para este usuário.")
        time.sleep(3)
    else:
        db_fernet = db.query_database("tokens", "user_id", user_id).fetchone()['token']
        dec_key = fc.dec_msg(db_fernet, query['service_key'])
        print(f"Senha para {entry} é: {dec_key}")
        time.sleep(3)
    #query.close()
    #db_fernet.close()

# Editar entradas
def edit_entry_password(user_id: int):
    # TODO
    # Encontrar o serviço pelo nome e trocar a senha   
    pass

# Deveria adicionar a função de excluir?

login = False

while True:
    user = []    
    clear_screen()
    print("""
    Password Saver - Salva senhas criptografadas.
    Comandos: sair, registrar, login.
    """)
    cmd_1 = input("-> ")
    match cmd_1.lower():
        case "sair":
            break
        case "registrar":
            new_user()
            continue
        case "login":
            user = user_login()
            if len(user) > 0:
                login = True
                while login:
                    clear_screen()
                    print(f"Logado como {user[1]}")
                    print("Comandos: criar, buscar, editar, sair")
                    cmd_2 = input("-> ")
                    match cmd_2.lower():
                        case "sair":
                            break
                        case "criar":
                            create_entry(user[1], user[0])
                            continue
                        case "buscar":
                            query = input("Nome do serviço que deseja buscar: ")
                            find_entry_by_name(user[0], query)
                            continue
                        case "editar":
                            pass
            continue


