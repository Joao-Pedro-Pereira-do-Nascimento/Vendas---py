import sqlite3

class DatabaseManager:
    def __init__(self):
        try:
            import sqlite3
        except ImportError:
            print("Erro ao importar o módulo sqlite3")

        # Conectar ao banco de dados ou criar um novo arquivo de banco de dados se ele não existir
        self.conn = sqlite3.connect('Database/store.db')
        self.c = self.conn.cursor()

    def create_product(self):
        name = input("Qual o nome do produto?\n")
        preco = float(input("Qual o valor de compra do produto?\n"))
        estoque = float(input(f"Quantos {name} foram comprados?\n"))
        precoV = float(input(f"Qual valor de venda do produto {name}\n"))
        lucro = (precoV * estoque) - (preco * estoque)

        # Inserir o nome e o preço na tabela 'inventory'
        sql = "INSERT INTO inventory (name, precoC, precoV, estoque, lucro) VALUES (?, ?, ?, ?, ?)"
        parameters = (name, preco, precoV, estoque, lucro)
        self.c.execute(sql, parameters)
        self.conn.commit()
        print("\033[93mProduto inserido com sucesso !!\033[0m")

    def get_max_id(self):
        result = self.c.execute('SELECT MAX(id) FROM inventory')

        for i in result:
            id = i[0]
            return id

    def close_connection(self):
        # Fechar a conexão com o banco de dados
        self.conn.close()

if __name__ == "__main__":
    # Criar uma instância da classe DatabaseManager
    db_manager = DatabaseManager()

    # Chamar o método create_product para inserir um produto
    db_manager.create_product()

    # Obter o ID máximo após a inserção
    max_id = db_manager.get_max_id()
    print(f"Produto foi inserido com ID : {max_id}°")

    # Fechar a conexão com o banco de dados
    db_manager.close_connection()
