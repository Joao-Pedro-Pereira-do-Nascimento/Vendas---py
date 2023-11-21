import sqlite3
import pwinput
import time

class ADM_USER:
    def __init__(self):
        try:
            import sqlite3
        except ImportError:
            print("Erro ao importar o módulo sqlite3")

        self.conn = sqlite3.connect('Database/security.db')
        self.c = self.conn.cursor()
        self.conn.commit()

    def listar_usuarios(self):
        result = self.c.execute('SELECT id, user, senha, cargo FROM login')

        # Imprimir cabeçalho com cores
        print("\033[1m{:<3} {:<17} {:<11} {:<15}\033[0m".format("ID", "User", "Senha", "Cargo"))
        print("\033[34m" + "=" * 65 + "\033[0m")  # Linha divisória azul

        # Iterar sobre os resultados e imprimir
        for row in result:
            id, user, senha, cargo = (
                "\033[32m" + str(row[0]) + "\033[0m" if row[0] is not None else "",
                row[1] if row[1] is not None else "",
                "\033[33m" + row[2] + "\033[0m" if row[2] is not None else "",
                "\033[36m" + str(row[3]) + "\033[0m" if row[3] is not None else ""

            )
            # Imprimir dados formatados com cores e alinhamento
            print("\033[1m{:<5} {:<20} {:<20} {:<15}\033[0m".format(id, user, senha, cargo))

    def modificar_usuario_interativo(self):
        try:
            self.listar_usuarios()  # Lista os usuários para que o usuário escolha o ID a ser modificado
            user_id = int(input("Digite o ID do usuário que deseja modificar (ou 0 para cancelar): "))

            if user_id == 0:
                print("Operação cancelada.")
                return

            self.c.execute('SELECT * FROM login WHERE id=?', (user_id,))
            usuario = self.c.fetchone()

            if usuario:
                print(f"\nDetalhes do usuário com ID {user_id}: {usuario}")
                escolha = input("\nDeseja realmente modificar este usuário? (s/n): ").lower()
                while escolha != "s" and escolha != 'n':
                    print("Digite uma opção valida")
                    time.sleep(2)
                    escolha = input("\nDeseja realmente modificar este usuário? (s/n): ").lower()

                if escolha == 's':
                  # Obtendo as novas informações do usuário
                    novo_user = input("Digite o novo user (deixe em branco para manter o valor atual): ").strip()
                    nova_senha = pwinput.pwinput("Digite a nova senha (deixe em branco para manter o valor atual): ").strip()
                    novo_cargo = input("Digite o novo cargo (deixe em branco para manter o valor atual):\n\033[93mADM\033[0m para administrador ou \033[93mFUNC\033[0m para funcionário: ").strip().upper()

                    # Verificando se algo foi digitado, caso contrário, mantenha os valores atuais
                    if not novo_user:
                        novo_user = usuario[4]  # Valor atual na tabela do bd

                    if not nova_senha:
                        nova_senha = usuario[5]  # Valor atual na tabela do bd

                    while novo_cargo not in {"ADM", "FUNC", ""}:
                        print("Atenção cargo inválido")
                        novo_cargo = input("Digite o cargo (deixe em branco para manter o valor atual):\n\033[93mADM\033[0m para administrador ou \033[93mFUNC\033[0m para funcionário: ").strip().upper()

                    # Executar a instrução SQL UPDATE
                    self.c.execute('UPDATE login SET user=?, senha=?, cargo=? WHERE id=?', (novo_user, nova_senha, novo_cargo, user_id))

                    self.conn.commit()
                    print(f"\033[93mUsuário com ID {user_id} modificado com sucesso.\033[0m")
                else:
                    print("Operação cancelada.")
            else:
                print(f"\033[91mUsuário com ID {user_id} não encontrado.\033[0m")

        except Exception as e:
            print(f"\033[91mErro ao modificar usuário: {e}\033[0m")

# Criar uma instância da classe DatabaseManager
db_manager_adm = ADM_USER()

# Exemplo de chamada da função para modificar um usuário de forma interativa
#db_manager_adm.modificar_usuario_interativo()

# Exemplo de chamada da função para listar usuários após a modificação
#db_manager_adm.listar_usuarios() #está comentado para abrir só dentro de menur_adm
