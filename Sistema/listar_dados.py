import sqlite3
import os

def buscar_produto(conn, nome):
    def limpar_tela():
        os.system('clear' or 'cls')

    limpar_tela()

    c = conn.cursor()

    if nome:  # Verifica se o campo de pesquisa não está vazio
        c.execute("SELECT * FROM inventory WHERE name=?", (nome,))
    else:
        c.execute("SELECT * FROM inventory")

    data = c.fetchall()

    if data:
        # Imprimir cabeçalho com cores
        print("\033[1m{:<12} {:<17} {:<15} {:<17} {:<13} {:<10}\033[0m".format(
            "ID", "Nome", "Preço Compra", "Preço Venda", "Estoque", "Lucro"
        ))
        print("\033[34m" + "="*120 + "\033[0m")  # Linha divisória azul

        for row in data:
            # Verificar se os valores são nulos e substituir por uma string vazia
            id, nome, preco_c, preco_v, estoque, lucro = (
                "\033[32m" + str(row[0]) + "\033[0m" if row[0] is not None else "",
                row[1] if row[1] is not None else "",
                "\033[33m" + f"R${row[2]:<14,.2f}" + "\033[0m" if row[2] is not None else "",
                "\033[33m" + f"R${row[3]:<14,.2f}" + "\033[0m" if row[3] is not None else "",
                "\033[36m" + str(row[4]) + "\033[0m" if row[4] is not None else "",
                "\033[32m" + f"R${row[7]:<14,.2f}" + "\033[0m" if row[7] is not None else ""
            )
            # Imprimir dados formatados com cores e alinhamento
            print("\033[1m{:<20} {:<20} {:<20} {:<20} {:<20} {:<20}\033[0m".format(
                id, nome, preco_c, preco_v, estoque, lucro
            ))
    else:
        if nome:
            print(f"\033[91mProduto com nome '{nome}' não encontrado.\033[0m")
        else:
            print("\033[91mNenhum produto encontrado.\033[0m")
    
    c.close()

if __name__ == "__main__":
    try:
        import sqlite3
    except ImportError:
        print("Erro ao importar o módulo sqlite3")

    # Conectar ao banco de dados ou criar um novo arquivo de banco de dados se ele não existir
    conn = sqlite3.connect('Database/store.db')

    # Exemplo de pesquisa por nome do produto
    nome_produto = input("Digite o nome do produto que deseja pesquisar (pressione Enter para mostrar todos :) ")
    buscar_produto(conn, nome_produto)

    # Fechar a conexão com o banco de dados
    conn.close()
