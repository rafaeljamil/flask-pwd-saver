from cryptography.fernet import Fernet
# Biblioteca de funções do Fernet

def create_key() -> str:
    return Fernet.generate_key()

def enc_msg(key: str, msg: str) -> str:
    fernet = Fernet(key)    
    enc_msg = fernet.encrypt(msg.encode())
    return enc_msg

def dec_msg(key: str, enc_msg:str) -> str:
    fernet = Fernet(key)
    dec_msg = fernet.decrypt(enc_msg)
    return dec_msg.decode('utf-8')


def run_test():
    f_key = create_key()
    print(f"{f_key=}")
    msg = "Uma mensagem de teste. ABC123"
    encrypted_msg = enc_msg(f_key, msg)
    print(f"{encrypted_msg=}")
    decrypted_msg = dec_msg(f_key, encrypted_msg)
    print(f"{decrypted_msg=}")

if __name__ == "__main__":
    run_test()
