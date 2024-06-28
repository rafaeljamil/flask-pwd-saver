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

test_user = ["fuleiro", "fuleiro123"]
test_token = [1, "token_do_fuleiro"]
test_service = [1, "netflix", "fuleiro123"]


if __name__ == '__main__':
    print("Biblioteca de interação com o banco de dados.")
    # create_tables() #rodando a primeira vez
    # insert_user(test_user)
    # insert_token(test_token)
    # insert_service(test_service)




    