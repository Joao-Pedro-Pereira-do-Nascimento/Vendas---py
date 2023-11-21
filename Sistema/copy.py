# vendas.py

import sqlite3

class Venda:
    def __init__(self, conn, c):
        self.conn = conn
        self.c = c
        self.produtos_venda = []

    def adicionar_produto(self, produto_id_nome, quantidade_venda):
        self.produtos_venda.append((produto_id_nome, quantidade_venda))

    def realizar_venda_individual(self, product_id, name, estoque_disponivel, preco_venda_unitario, quantidade_venda):
        if estoque_disponivel is not None and estoque_disponivel >= quantidade_venda:
            preco_total = quantidade_venda * preco_venda_unitario

            print(f"Produto ID: {product_id}, Nome: {name}, Estoque disponível: {estoque_disponivel}, Quantidade vendida: {quantidade_venda}, Preço total: {preco_total}")

            novo_estoque = estoque_disponivel - quantidade_venda
            self.c.execute("UPDATE inventory SET estoque=? WHERE id=?", (novo_estoque, product_id))
            self.conn.commit()

            if novo_estoque == 0:
                self.c.execute("DELETE FROM inventory WHERE id=?", (product_id,))
                self.conn.commit()

            return preco_total
        else:
            print("\033[91mEstoque insuficiente para realizar a venda.\033[0m")
            return 0

    def realizar_venda(self):
        total_venda = 0

        for produto_id_nome, quantidade_venda in self.produtos_venda:
            self.c.execute("SELECT id, name, estoque, precoV FROM inventory WHERE id=? OR name=?", (produto_id_nome, produto_id_nome))
            result = self.c.fetchall()

            if result:
                if len(result) == 1:
                    product_id, name, estoque_disponivel, preco_venda_unitario = result[0]
                    total_venda += self.realizar_venda_individual(product_id, name, estoque_disponivel, preco_venda_unitario, quantidade_venda)
                else:
                    print("\nExistem múltiplos produtos com o mesmo nome. Escolha o produto pelo ID:")
                    for product_id, name, estoque, precoV in result:
                        # Verificar se os valores são nulos e substituir por uma string vazia
                        id, nome, estoque, precoV = (
                            "\033[32m" + f"ID: {product_id}" + "\033[0m" if product_id is not None else "",
                            f"Nome: {name}" if name is not None else "",
                            "\033[36m" + f"Estoque: {estoque}" + "\033[0m" if estoque is not None else "",
                            "\033[33m" + f"Preço: R${precoV:.2f}" + "\033[0m" if precoV is not None else ""
                        )
                        # Imprimir dados formatados com cores e alinhamento
                        print("\033[1m{:<5} {:<3} {:<10} {:<5}\033[0m".format(
                            id, nome, estoque, precoV
                        ))
                    print()  # Adiciona uma linha em branco após os produtos



                    valid_id = False
                    while not valid_id:
                        chosen_id = int(input("Digite o ID do produto desejado: "))
                        if chosen_id in [item[0] for item in result]:
                            product_id, name, estoque_disponivel, preco_venda_unitario = next(item for item in result if item[0] == chosen_id)
                            total_venda += self.realizar_venda_individual(product_id, name, estoque_disponivel, preco_venda_unitario, quantidade_venda)
                            valid_id = True
                        else:
                            print("\033[91mID inválido. Tente novamente.\033[0m")
            else:
                print(f"\033[91mProduto com ID ou Nome {produto_id_nome} não encontrado.\033[0m")

        return total_venda

def executar_vendas():
    # Conectar ao banco de dados ou criar um novo arquivo de banco de dados se ele não existir
    conn = sqlite3.connect('Database/store.db')
    c = conn.cursor()

    venda = Venda(conn, c)

    while True:
        produto_id_nome = input("Digite o ID ou o Nome do produto que deseja vender (ou 'não' para encerrar):\n")

        if produto_id_nome.lower() == 'não':
            break

        quantidade_venda = float(input(f"Digite a quantidade de {produto_id_nome} que deseja vender:\n"))

        venda.adicionar_produto(produto_id_nome, quantidade_venda)

    # Realizar a venda apenas no final, após adicionar todos os produtos
    total_venda = venda.realizar_venda()

    # Agora você pode usar 'total_venda' para exibir o total antes de pedir o pagamento
    print(f"\033[33mTotal da venda: {total_venda}\033[0m")

    # Perguntar pelo método de pagamento apenas se houver uma venda
    if total_venda > 0:
        metodo_pagamento = input("Digite o método de pagamento (Dinheiro, Cartão, etc.): ").strip().lower()

        if metodo_pagamento == 'dinheiro':
            valor_pago = float(input("Digite o valor pago: "))
            troco = valor_pago - total_venda
            if troco < 0:
                print("\033[91mPagamento insuficiente. Venda não realizada.\033[0m")
            else:
                print(f"\033[92mVenda realizada com sucesso!\033[0m")
                print(f"Pagamento: {metodo_pagamento}, Troco: {troco}")
        elif metodo_pagamento == 'cartao':
            print("Cada \033[93mn\033[0m pacelas, aumenta em \033[93mn\033[0m por cento no valor do produto \n Exemplo: \033[93m10R$ em 10 pacelas é 11\033[0m")
            cart = int(input("Digite a quantidade de pacelas, com no máximo \033[93m[ 10 ]\033[0m\n"))        
            if cart > 10:
                print("\033[91mNúmero de parcelas inválido. Venda não realizada.\033[0m")
            else:
                match cart:
                    case 1:
                        valor_pago = total_venda + (total_venda*0.01)
                    case 2:
                        valor_pago = total_venda + (total_venda*0.02)
                    case 3:
                        valor_pago = total_venda + (total_venda*0.03)
                    case 4:
                        valor_pago = total_venda + (total_venda*0.04)
                    case 5:
                        valor_pago = total_venda + (total_venda*0.05)
                    case 6:
                        valor_pago = total_venda + (total_venda*0.06)
                    case 7:
                        valor_pago = total_venda + (total_venda*0.07)
                    case 8:
                        valor_pago = total_venda + (total_venda*0.08)
                    case 9:
                        valor_pago = total_venda + (total_venda*0.09)
                    case 10:
                        valor_pago = total_venda + (total_venda*0.1)
                
                print(f"\033[92mVenda realizada com sucesso!\033[0m")
                print(f"Pagamento: {metodo_pagamento}, Valor total: {valor_pago}")
        else:
            print(f"\033[92mVenda realizada com sucesso!\033[0m")
            print(f"Pagamento: {metodo_pagamento}")

    # Fechar a conexão com o banco de dados
    conn.close()
