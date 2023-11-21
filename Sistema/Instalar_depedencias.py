import subprocess
import sys
import platform
import time
import os

def limpar_tela():
    os.system('clear' if platform.system() == 'Linux' else 'cls')

def criar_ambiente_virtual():
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("Ambiente virtual criado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar ambiente virtual: {e}")

def instalar_pacotes():
    pacotes_necessarios = ["pwinput", "reportlab", "requests", "Pillow"]
    sistema_operacional = platform.system().lower()
    amarelo = '\033[1;33m'
    vermelho = '\033[1;31m'
    reset = '\033[0m'

    if sistema_operacional != 'linux':
        for pacote in pacotes_necessarios:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
                print(f"{pacote} instalado com sucesso.")
            except subprocess.CalledProcessError as e:
                print(f"{vermelho}Erro ao instalar {pacote}.{reset}")
                print(f"Erro: {e}")
    else:
        limpar_tela()
        print(f"Sistema operacional Linux 🐧 detectado.")
        print(f"{amarelo}Criando ambiente virtual...{reset}")
        criar_ambiente_virtual()

        for pacote in pacotes_necessarios:
            try:
                subprocess.check_call(["./venv/bin/python", "-m", "pip", "install", pacote])
                print(f"{pacote} instalado no ambiente virtual com sucesso.")
            except subprocess.CalledProcessError as e:
                print(f"{vermelho}Erro ao instalar {pacote} no ambiente virtual.{reset}")
                print(f"Erro: {e}")

        print(f"Ambiente virtual criado. Considere ativá-lo com {amarelo}'source venv/bin/activate'.{reset}")
        time.sleep(10)
        limpar_tela()

def setup_ambiente():
    instalar_pacotes()

if __name__ == "__main__":
    setup_ambiente()
