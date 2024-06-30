import os
import sqlite3

def connect_to_database() -> object:
    db = sqlite3.connect("info.db")
    return db

# Connection test
#con = connect_to_database()
#print(con)
#print(type(con))

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

def insert_token(data: list) -> None: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    cursor.execute("INSERT INTO tokens(user_id, token) VALUES(?,?)", (data[0], data[1]))
    con.commit()

def insert_service(data: list) -> None: #Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    cursor.execute("INSERT INTO services(user_id, service_name, service_key) VALUES(?, ?, ?)", (data[0], data[1], data[2]))
    con.commit()

def query_database(table: str, column: str, query: str|int) -> object: # Funcionando
    con = connect_to_database()
    cursor = con.cursor()
    query_end = f"'{query}'" if type(query) == str else f"{query}" # fazendo a query funcionar com strings e integers
    query_str = f"SELECT * FROM {table} WHERE {column} = " + query_end # com fstring funciona. Precisa das aspas simples no query.
    return cursor.execute(query_str)



# TESTS

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
        ("services", "service_name", "netflix")
]
    for row in data:
        #print(row[0])
        query = query_database(row[0], row[1], row[2])
        print(query.fetchone())

if __name__ == '__main__':
    print("Biblioteca de interação com o banco de dados.")
    # create_tables() #rodando a primeira vez
    # test_database_insert()
    # test_query_database()




    
