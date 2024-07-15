# CLI para testes e configurações.
import app_commands as commands
import os
import time

# Organizando Funções

# Limpar tela do terminal
def clear_screen() -> None:
    if os.uname().sysname == "Linux":
        os.system("clear")
    else:
        os.system("cls")

def new_user() -> None:
    clear_screen()
    username = input("Escolha um nome de usuário: ")
    password = input("Escolha uma senha: ")
    print(f"Você escolheu {username} como usuário e {password} como senha.")    
    if input("Você confirma os dados acima? ").lower() in ["yes", "y", "sim", "s"]:
        response = commands.new_user(username, password)
        print("Usuário criado.") if response["create_user"] == 0 else print("Erro na criação de usuário.")
        print("Token salvo.") if response["create_token"] == 0 else print("Erro na criação do token.")
        time.sleep(3)
#        user_key = fc.create_key()
#        enc_pwd = fc.enc_msg(user_key, password)
#        user_info = [username, enc_pwd]
#        db.insert_user(user_info)
#        print("Usuário criado.")
#        user = db.get_user_by_username(username) # buscando em users por username
#        user_id = user['id']        
#        db.insert_token([user_id, user_key])
#        print("Token salvo.")
    else:
        print("Dados não confirmados. Cancelando ação.")
        time.sleep(3)

# fazer login do usuário
def user_login() -> list:
    # Pega input de usuário e senha, checa o banco de dados pra ver se está correto e retorna uma lista com informações do usuário
    username = input("Usuário -> ")
    password = input("Senha -> ")
    response = commands.user_login(username, password)
    if response["user"] == -1:
        print("Usuário não encontrado.")
        time.sleep(3)
        return []
    else:
        if response["data"] == -1:
            print("Senha inválida...")
            time.sleep(3)
            return []
        else:
            user_info = [v for v in response["data"].values()] #[user_id, username]
            return user_info
    

# Nova entrada de serviço, site ou app e a respectiva senha criptografada
def create_entry(user_data:list) -> None:
    # user_data = [user_id, username]
    service = input("Nome do serviço, site ou app: ")
    svc_pwd = input("Senha do serviço, site ou app: ")
    usr_pwd = input("Confirme a senha de usuário: ")

    entry_data = [user_data[0], user_data[1], service, svc_pwd, usr_pwd]
    entry = commands.create_entry(entry_data)

    if entry == 0:
        print("Nova entrada salva com sucesso.")
        time.sleep(3)
    else:
        print("Senha inválida...")
        time.sleep(3)


# Buscar serviço, site ou app, decripta a senha salva no banco e mostra pro usuário
def find_entry_by_name(user_id: int, entry: str) -> None:
    # buscando todas as chaves do usuário logado pra encontrar o serviço que ele quer. Se buscar por serviço pode vazar dados de outros usuários.
    q_data = [user_id, entry]
    query = commands.find_entry_by_name(q_data)
    if query == None:
        print("Serviço, site ou app não encontrado para este usuário.")
        time.sleep(3)
    else:
        print(f"Senha para {entry} é: {query}")
        time.sleep(3)


# Editar entradas
def edit_entry_password(user: list) -> None:
    service = input("Nome do serviço, site ou app: ") 
    query = commands.check_entry([user[0], service])
    if query == None: # Checando se existe um serviço, site ou app salvo com esse nome no banco
        print(f"Este usuário não tem nenhuma senha salva para {service}.")
        time.sleep(3)
    else:
        svc_pwd = input("Nova senha do serviço, site ou app: ")
        usr_pwd = input("Confirme a senha de usuário: ") 
        entry_data = [user[0], user[1], service, svc_pwd, usr_pwd]
        entry = commands.edit_entry_password(entry_data)
        if entry == 0:
            print(f"Senha para {service} atualizada com sucesso.")
            time.sleep(3)
        else:
            print("Senha não modificada")
            time.sleep(3)

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
                    print("Comandos: criar, buscar, editar, voltar")
                    cmd_2 = input("-> ")
                    match cmd_2.lower():
                        case "voltar":
                            break
                        case "criar":
                            create_entry(user)
                            continue
                        case "buscar":
                            query = input("Nome do serviço que deseja buscar: ")
                            find_entry_by_name(user[0], query)
                            continue
                        case "editar":
                            edit_entry_password(user)
                            continue
            continue


