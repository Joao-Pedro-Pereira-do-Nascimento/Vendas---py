import sqlite3
import pwinput
from menur_vendedor import main_vend
from menur_adm import main_adm
from intro import *
import time
import os
import platform
def limpar_tela():
    os.system('clear' if platform.system() == 'Linux' else 'cls')   
class Cor:
    amarelo = '\033[1;33m'
    tag = '\033[m'
    reset = '\033[0m'

def temporizador(segundos):
    for i in range(segundos, 0, -1):        
        limpar_tela()
        print(f"Tempo restante: {Cor.amarelo}{i}{Cor.reset} segundos")
        time.sleep(1)
    limpar_tela()
    print(f"{Cor.amarelo}Tente novamente{Cor.reset}")
    time.sleep(1.5)
    limpar_tela()
    login_obj.verificacao()
class Login:
    def __init__(self):
        try:
            import sqlite3
        except ImportError:
            print("Erro ao importar o módulo sqlite3")

        self.conn = sqlite3.connect('Database/security.db')
        self.c = self.conn.cursor()        
        
    def verificacao(self):
        tentativa = 0
        while tentativa < 3:
            limpar_tela()
            user = input("Usuário:")
            senha = pwinput.pwinput("Senha:")

            if user and senha:
                # Use uma consulta parametrizada para evitar SQL injection
                self.c.execute("SELECT * FROM login WHERE user=? AND senha=?", (user, senha))
                resultado = self.c.fetchone()

                if resultado:
                    print("Login bem-sucedido!")
                    # Verifique o cargo do usuário logado
                    self.c.execute("SELECT cargo FROM login WHERE user=?", (user,))
                    resultado_cargo = self.c.fetchone()

                    if resultado_cargo:
                        cargo = resultado_cargo[0]
                        print(f"Cargo: {cargo}")

                        if cargo == 'ADM':
                            print(f"O {user} tem cargo de Administrador.")
                            time.sleep(3)
                            limpar_tela()
                            iniciar_intro()
                            main_adm()
                        elif cargo == 'FUNC':
                            print(f"O {user} tem cargo de Funcionário.")
                            time.sleep(3)
                            limpar_tela()
                            iniciar_intro()
                            main_vend()
                        else:
                            print("Cargo desconhecido.")
                    
                    break  # Sair do loop se o login for bem-sucedido
                else:
                    print(f"O User ({Cor.amarelo}{user}{Cor.reset}) ou a Senha ({Cor.amarelo}{senha}{Cor.reset}) está incorreto")
                    time.sleep(1.5)
                    tentativa += 1
                    if tentativa == 3:
                        limpar_tela()
                        print(f"{Cor.amarelo}Devido a quantidadde de tentativa, espere 5 segundos para tentar novamente{Cor.reset}")        
                        time.sleep(2)
                        temporizador(5)  # Defina o número de segundos para o temporizador
            else:
                print("Usuário ou senha incorretos.")
        else:
            print("Usuário ou senha não fornecidos.")

        self.conn.commit()

# Exemplo de uso
if __name__ == "__main__":
    login_obj = Login()
    login_obj.verificacao()
