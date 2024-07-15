# Lib de comandos para front-end e CLI
import fernet_commands as fc
import database_commands as db

# NOVO USUARIO
def new_user(username:str, password:str) -> dict:
    resp = dict()    
    user_key = fc.create_key()
    enc_pwd = fc.enc_msg(user_key, password)
    user_info = [username, enc_pwd]
    db.insert_user(user_info)
    resp["create_user"] = 0
    user = db.get_user_by_username(username) # buscando em users por username
    user_id = user['id']        
    db.insert_token([user_id, user_key])
    resp["create_token"] = 0
    return resp

# LOGIN USUARIO
def user_login(username, password) -> dict:
    resp = dict()
    db_user = db.get_user_by_username(username) # buscando em users por username
    if db_user == None:
        resp["user"] = -1
    else:
        resp["user"] = 0
        resp["data"] = dict()
        db_fernet = db.get_user_token(db_user['id']) #buscando em tokens por user_id
        dec_pwd = fc.dec_msg(db_fernet['token'], db_user['password'])
        if password == dec_pwd:
            resp["data"]["user_id"] = db_user["id"]
            resp["data"]["username"] = username
            user_info = [db_user['id'], username]
        else:
            resp["data"] = -1
    return resp

# CRIAR ENTRADA
# Verificar senha do usuario
def check_password(data: list) -> bool:
    user_id = data[0]
    username = data[1]
    usr_pwd = data[2]
    db_user = db.get_user_by_username(username) # buscando em users por username 
    db_fernet = db.get_user_token(user_id) # buscando em tokens por user_id
    dec_pwd = fc.dec_msg(db_fernet["token"], db_user["password"])
    return True if usr_pwd == dec_pwd else False

# Criar senha encriptada
def create_password(data: list) -> str:
    user_id = data[0]
    svc_pwd = data[1]
    db_fernet = db.get_user_token(user_id)
    enc_svc_pwd = fc.enc_msg(db_fernet["token"], svc_pwd)
    return enc_svc_pwd

# Salvar novo serviço no banco de dados
def create_entry(data: list) -> int:
    user_id = data[0]
    username = data[1]
    service = data[2]
    svc_pwd = data[3]
    usr_pwd = data[4]
    check_data = [user_id, username, usr_pwd]

    if check_password(check_data):
        # Ao confirmar com senha, o processo de criptografia começa
        pwd_data = [user_id, svc_pwd]
        enc_svc_pwd = create_password(pwd_data)
        data = [user_id, service, enc_svc_pwd]
        db.insert_service(data)
        return 0
    else:
        return -1

# ENCONTRAR ENTRADA POR NOME
def find_entry_by_name(data: list) -> str:
    # buscando todas as chaves do usuário logado pra encontrar o serviço que ele quer. Se buscar por serviço pode vazar dados de outros usuários.
    user_id = data[0]    
    entry = data[1]
    query = db.get_service(entry, user_id)
    if query == None:
        return query
    else:
        db_fernet = db.query_database("tokens", "user_id", user_id).fetchone()['token']
        dec_key = fc.dec_msg(db_fernet, query['service_key'])
        return dec_key

# EDITAR ENTRADAS
def check_entry(data: list) -> int:
    user_id = data[0]
    service = data[1]  
    query = find_entry_by_name([user_id, service])
    if query == None: # Checando se existe um serviço, site ou app salvo com esse nome no banco
        return -1
    else:
        return 0

def edit_entry_password(data: list) -> None:
    user_id = data[0]
    username = data[1]
    service = data[2]
    svc_pwd = data[3]
    usr_pwd = data[4]
    check_data = [user_id, username, usr_pwd]

    if check_password(check_data):
        # Ao confirmar com senha, o processo de criptografia começa
        if check_entry([data[0], data[2]]) == 0:
            pwd_data = [user_id, svc_pwd]
            enc_svc_pwd = create_password(pwd_data)
            data = [user_id, service, enc_svc_pwd]
            db.update_service(data)
            return 0
        else:
            return -1




