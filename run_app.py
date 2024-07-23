# Ferramenta pra rodar o app do flask
import os
import database_commands as db

system = os.uname().sysname

def run_flask_app() -> None:
    command: str = ""

    if not os.path.isfile("/info.db"):
        print("Criando banco de dados...")
        try:        
            db.create_tables()
            print("Banco de dados criado.")
        except:
            print("Erro na criação do banco de dados.")

    if system == "Linux":
        command = "python3 -m flask --app app run"
    else:
        command = "python -m flask --app app run"
    cmd_debug: str = command + " --debug"
    # os.system(command) # roda sem debug
    os.system(cmd_debug) # roda com debug

if __name__ == "__main__":
    run_flask_app()
