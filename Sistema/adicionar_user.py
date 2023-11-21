import sqlite3
import pwinput
from datetime import datetime
import time
class DatabaseManager:
    def __init__(self):
        try:
            import sqlite3
        except ImportError:
            print("Erro ao importar o módulo sqlite3")

        self.conn = sqlite3.connect('Database/security.db')
        self.c = self.conn.cursor()
        self.conn.commit()

    def adicionar_user(self):
        nomeC = input("Qual o nome do novo funcionário?\n")
        cpf = (input(f"Qual o cpf do(a) {nomeC}?\n"))
        while len(cpf) != 11:
            print(f"\033[91mO CPF deve conter 11 dígitos do tipo inteiro, você digitou com (\033[93m{len(cpf)}\033[0m) preencha novamente\033[0m")
            cpf = input(f"Qual o cpf do(a) {nomeC}?\n")
        anoNascimento = int(input(f"Qual ano o {nomeC} nasceu ?\n"))
        ano_atual = datetime.now().year
        idade =  ano_atual - anoNascimento
        while idade <= 14 or idade >=120:
            print("\033[91m{0} idade não permitida, lembre de colocar uma idade maior ou igual a 15 e menor que 120 anos\033[0m".format(idade))
            time.sleep(1)
            anoNascimento = int(input(f"Qual ano o {nomeC} nasceu ?\n"))
            ano_atual = datetime.now().year
            idade =  ano_atual - anoNascimento
        user = input(f"Qual o user do {nomeC}\n")
        senha = pwinput.pwinput(f"Qual a senha do {user}: \n")
        cargo = input(f"Digite o cargo do {nomeC}:\n\033[93mADM\033[0m para administrador ou \033[93mFUNC\033[0m para funcionário:\n").upper()
        while  cargo != "ADM" and cargo != "FUNC":
            print("Atenção cargo invalido")
            cargo = input(f"Digite o cargo do {nomeC}:\n\033[93mADM\033[0m para administrador ou \033[93mFUNC\033[0m para funcionário:\n").upper()
            

        # Inserir o nome e o preço na tabela 'inventory'
        sql = "INSERT INTO login (nomeC, cpf, idade, user, senha, cargo) VALUES (?, ?, ?, ?, ?, ?)"
        parameters = (nomeC, cpf, idade, user, senha, cargo)
        self.c.execute(sql, parameters)
        self.conn.commit()
        print("\033[93mNovo Funcionário adicionado com Sucesso!!!!!!\033[0m")

    def get_max_id(self):
        result = self.c.execute('SELECT MAX(id) FROM login')

        for i in result:
            id = i[0]
            return id

# Criar uma instância da classe DatabaseManager
db_manager = DatabaseManager()

# Exemplo de chamada da função
#db_manager.adicionar_user()
