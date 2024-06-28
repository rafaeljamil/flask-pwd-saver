# Ferramenta pra rodar o app do flask
import os

def run_flask_app() -> None:
    command: str = "python -m flask --app app run"
    cmd_debug: str = command + " --debug"
    # os.system(command) # roda sem debug
    os.system(cmd_debug) # roda com debug

if __name__ == "__main__":
    run_flask_app()