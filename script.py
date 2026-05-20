import requests
import hashlib
import os

def sys(string):
    os.system(string)



BANNER = """
  █████   █    ██  ▄▄▄      ▓█████▄  ██▀███   ▄▄▄      ▓█████▄  ▒█████   ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀▓█████  ██▀███  
▒██▓  ██▒ ██  ▓██▒▒████▄    ▒██▀ ██▌▓██ ▒ ██▒▒████▄    ▒██▀ ██▌▒██▒  ██▒▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▒██▒  ██░▓██  ▒██░▒██  ▀█▄  ░██   █▌▓██ ░▄█ ▒▒██  ▀█▄  ░██   █▌▒██░  ██▒▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
░██  █▀ ░▓▓█  ░██░░██▄▄▄▄██ ░▓█▄   ▌▒██▀▀█▄  ░██▄▄▄▄██ ░▓█▄   ▌▒██   ██░░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
░▒███▒█▄ ▒▒█████▓  ▓█   ▓██▒░▒████▓ ░██▓ ▒██▒ ▓█   ▓██▒░▒████▓ ░ ████▓▒░░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░ ▒▒▓  ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒▒▓  ▒ ░ ▒░▒░▒░  ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ▒░  ░ ░░▒░ ░ ░   ▒   ▒▒ ░ ░ ▒  ▒   ░▒ ░ ▒░  ▒   ▒▒ ░ ░ ▒  ▒   ░ ▒ ▒░  ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
   ░   ░  ░░░ ░ ░   ░   ▒    ░ ░  ░   ░░   ░   ░   ▒    ░ ░  ░ ░ ░ ░ ▒   ░  ░░ ░  ░   ▒   ░        ░ ░░ ░    ░     ░░   ░ 
    ░       ░           ░  ░   ░       ░           ░  ░   ░        ░ ░   ░  ░  ░      ░  ░░ ░      ░  ░      ░  ░   ░     
                             ░                          ░                                 ░                               
"""

SUPABASE_URL = "https://vqqvfvtuikpohzuzgymb.supabase.co"
SUPABASE_KEY = "sb_publishable_EV20V63Y2rjUscWHu28rbA_irMTciZk"


endpoint = f"{SUPABASE_URL}/rest/v1/jogadores"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def generar_hash_senha(senha_pura: str) -> str:
    msg_buffer = senha_pura.encode('utf-8')
    hash_objeto = hashlib.sha256(msg_buffer)
    return hash_objeto.hexdigest()

def injetar_stats(nickname: str, senha_pura: str):
    senha = generar_hash_senha(senha_pura)
    payload = {
        "nickname": nickname,
        "senha": senha,
        "val": 5000,
        "inc": 5,
        "mul": 1,
        "auto": 2,
        "total": 5000,
        "upgrades": [
            {"id": "up1", "custo": 13, "ganho": 1, "multiplicador": 1.3}
        ],
        "autos": [],
        "multi": []
    }

    endpoint_upsert = f"{endpoint}?on_conflict=nickname"

    resposta = requests.post(endpoint_upsert, json=payload, headers=headers)
    
    if resposta.status_code in [200, 201]:
        print("yeah we did it")
    else:
        print(f"Erro: {resposta.text}")

    
def puxar_dados():
    params = {
        "select": "*"
    }
    
    response = requests.get(endpoint, headers=headers, params=params) 

    if response.status_code == 200:
        dados = response.json()
        if not dados:
            print("Nenhum jogador encontrado na tabela.")
        for jogador in dados:
            print(f"Nick: {jogador.get('nickname')} - Hash: {jogador.get('senha')}")
    else:
        print(f"Erro na requisição: {response.status_code}")
        print(response.text)

def main():
    while True:
        print(BANNER)
        print("\nEscolhas:\n[1]-Injetar Status\n[2]-Puxar dados\n")
        escolha = int(input("> "))
        
        if escolha == 1:
            nickname = input("(nickname-alvo) > ")
            senha = input("(sua-senha) > ")
            sys("clear")
            injetar_stats(nickname, senha)
            input()
            sys("clear")
            
        elif escolha == 2: 
            sys("clear")
            puxar_dados()
            input()
            sys("clear")
            

main()
        
                
