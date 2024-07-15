import os
import sqlite3

def connect_to_database() -> object:
    db = sqlite3.connect("info.db")
    db.row_factory = sqlite3.Row
    return db

# Connection test
#con = connect_to_database()
#print(con)
#print(type(con))

#----------------------------------------#
# Criação do banco de dados e das tabelas
def create_tables() -> None: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    cursor.executescript("""
        BEGIN;
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username UNIQUE, password);
        CREATE TABLE IF NOT EXISTS tokens (id INTEGER PRIMARY KEY, user_id, token, FOREIGN KEY (user_id) REFERENCES user(id));
        CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY, user_id, service_name, service_key, FOREIGN KEY (user_id) REFERENCES user(id));
        COMMIT;
""")
    # print("Banco de dados criado com sucesso.")

def insert_user(data: list) -> None: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    cursor.execute("INSERT INTO users(username, password) VALUES(?, ?)", (data[0], data[1]))
    con.commit()
    con.close()

def insert_token(data: list) -> None: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    cursor.execute("INSERT INTO tokens(user_id, token) VALUES(?,?)", (data[0], data[1]))
    con.commit()
    con.close()

def insert_service(data: list) -> None: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    cursor.execute("INSERT INTO services(user_id, service_name, service_key) VALUES(?, ?, ?)", (data[0], data[1], data[2]))
    con.commit()
    con.close()

def update_service(data: list) -> None:
    con = connect_to_database()
    cursor = con.cursor()
    cursor.execute("UPDATE services SET service_key = ? WHERE service_name = ? AND user_id = ?", (data[2], data[1], data[0])) # [new service key, service name, user id]
    con.commit()
    con.close()

#----------------------------------------#
# Queries
# SELECT user
def get_user_by_username(username: str) -> list: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    db_response = cursor.execute("SELECT rowid, password FROM users WHERE username = ?", (username,)) #rowid volta como key 'id'
    return db_response.fetchone()

# SELECT service by service_name and user_id
def get_service(service_name: str, user_id: int) -> list: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    db_response = cursor.execute("SELECT service_key FROM services WHERE service_name = ? AND user_id = ?", (service_name, user_id))
    return db_response.fetchone()

# SELECT token
def get_user_token(user_id: int) -> list: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    db_response = cursor.execute("SELECT token FROM tokens WHERE user_id = ?", (user_id,))
    return db_response.fetchone()


def query_database(table: str, column: str, query: str|int) -> object: # Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    query_end = f"'{query}'" if type(query) == str else f"{query}" # fazendo a query funcionar com strings e integers
    query_str = f"SELECT * FROM {table} WHERE {column} = " + query_end # com fstring funciona. Precisa das aspas simples no query.
    db_response = cursor.execute(query_str)
    #con.close()     
    return db_response

def query_database_script(script: str) -> object: # Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    query_str = f"""{script}"""
    db_response = cursor.execute(query_str)
    #con.close()     
    return db_response

#----------------------------------------#
# TESTES
# insert tests
test_user = ["fuleiro", "fuleiro123"]
test_token = [1, "token_do_fuleiro"]
test_service = [1, "netflix", "fuleiro123"]

def test_database_insert() -> None:
    insert_user(test_user)
    insert_token(test_token)
    insert_service(test_service)

# query tests
def test_query_database() -> None:
    data: list = [
        ("users", "username", "fuleiro"),
        ("tokens", "user_id", 1),
        ("services", "service_name", "netflix"),
        ("users", "username", "ciclano")
]
    for row in data:
        #print(row[0])
        query = query_database(row[0], row[1], row[2])
        #print(query)        
        print(query.fetchone())

def test_query_database_script():
    #db_script = "SELECT * FROM services"
    db_script = "SELECT * FROM services WHERE user_id = 1 AND service_name = 'netflix'"
    query = query_database_script(db_script)
    result = query.fetchone()
    print(result['service_name'])

def test_select_func():
    query_user = get_user_by_username("teste")
    query_service = get_service("netflix", 1)
    query_token = get_user_token(1)
    print(f"{query_user['password']=}")
    print(query_service['service_key']) # funciona com query[0] também
    print(f"{query_token['token']=}")

if __name__ == '__main__':
    print("Biblioteca de interação com o banco de dados.")
    # create_tables() #rodando a primeira vez
    # test_database_insert()
    # test_query_database()
    # test_query_database_script()
    test_select_func()




    
