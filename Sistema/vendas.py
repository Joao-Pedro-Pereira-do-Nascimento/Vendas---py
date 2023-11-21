import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from PIL import Image

class Venda:
    def __init__(self, conn, c):
        self.conn = conn
        self.c = c
        self.produtos_venda = []
        self.cart = None

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

    def criar_nota_fiscal_pdf(self, total_venda, metodo_pagamento):
        # Obter a data e hora atual
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M")

        # Criar um arquivo PDF
        pdf = canvas.Canvas(f"Notas_Fiscais/Nota_Fiscal_{data_hora}.pdf", pagesize=letter)

        # Adicionar informações à nota fiscal
       
        pdf.setFont('Courier-Bold', 14)
        pdf.drawString(220, 770, "Nota Fiscal")
        pdf.setFont('Courier-Bold', 12)
        pdf.drawString(130, 750, f"Data e Hora: {data_hora} da Compra")
        if metodo_pagamento =='cartao':
            pdf.drawString(130, 730, f"Valor Total Pago: R${total_venda} em {self.cart} vezes no {metodo_pagamento.upper()}")
        else:
             pdf.drawString(130, 730, f"Valor Total Pago: R${total_venda} no {metodo_pagamento.upper()}")

        y_coord = 700  # Coordenada Y inicial
        for produto_id_nome, quantidade_venda in self.produtos_venda:
            self.c.execute("SELECT name, precoV FROM inventory WHERE id=? OR name=?", (produto_id_nome, produto_id_nome))
            result = self.c.fetchone()
            if result:
                name, preco_unitario = result
                pdf.setFont('Courier-Bold', 8)
                pdf.drawString(220, y_coord, f"Produto: {name}")
                pdf.drawString(220, y_coord - 12, f"Quantidade: {quantidade_venda}")
                pdf.drawString(220, y_coord - 24, f"Preço Unitário: R${preco_unitario:.2f}")
                if metodo_pagamento == 'cartao':
                    pdf.drawString(220, y_coord - 36, f"Valor Total Pago: R${quantidade_venda*preco_unitario}")
                    pdf.drawString(220, y_coord - 48, f"Método de pagamento {metodo_pagamento.upper()}")
                    pdf.drawString(0, y_coord - 53, "...............................................................................................................................................................................")
                else:
                    pdf.drawString(220, y_coord - 36 , f"Valor Total Pago: R${quantidade_venda*preco_unitario}")
                    pdf.drawString(220, y_coord - 48, f"Método de Pagamento: {metodo_pagamento.upper()}")
                    pdf.drawString(0, y_coord - 53, "...............................................................................................................................................................................")

                
                y_coord -= 59  # Diminuir a coordenada Y para o próximo produto
                pdf.drawString(200, 83, f"Código de Barras:")
                
        icon = "img/icon_lampada.png"  
        pdf.drawInlineImage(icon, 500, 693, width=100, height=100)          
        seguranca = "img/seguranca.png"  
        pdf.drawInlineImage(seguranca, 100, 120, width=420, height=210)
        qrcode_path = "img/qrcode-pix.png"  
        pdf.drawInlineImage(qrcode_path,510, 10, width=100, height=100)
        qrcodeo2_path = "img/codbarras.png"  
        pdf.drawInlineImage(qrcodeo2_path, 15, 12, width=480, height=60)  
       


        # Salvar o arquivo PDF
        pdf.save()

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

        # Agora você pode usar 'total_venda' para exibir o total antes de pedir o pagamento
        print(f"\033[33mTotal da venda: {total_venda}\033[0m")

        # Perguntar pelo método de pagamento apenas se houver uma venda
        if total_venda > 0:
            metodo_pagamento = input("Digite o método de pagamento (Dinheiro, Cartão, etc.): ").strip().lower()
            while metodo_pagamento not in ['dinheiro', 'cartao']:
                print("Digite \033[93mdinheiro\033[0m ou \033[93mcartao\033[0m")
                metodo_pagamento = input("Digite o método de pagamento (Dinheiro, Cartão, etc.): ").strip().lower()

            if metodo_pagamento == 'dinheiro':
                valor_pago = float(input("Digite o valor pago: "))
                troco = valor_pago - total_venda
                if troco < 0:
                    print("\033[91mPagamento insuficiente. Venda não realizada.\033[0m")
                else:
                    print(f"\033[92mVenda realizada com sucesso!\033[0m")
                    print(f"Pagamento: {metodo_pagamento}, Troco: {troco}")
                    # Chamar o método para criar a nota fiscal em PDF
                    self.criar_nota_fiscal_pdf(total_venda, metodo_pagamento)
            elif metodo_pagamento == 'cartao':
                print("Cada \033[93mn\033[0m pacelas, aumenta em \033[93mn\033[0m por cento no valor do produto \n Exemplo: \033[93m10R$ em 10 pacelas é 11\033[0m")
                cart = int(input("Digite a quantidade de pacelas, com no máximo \033[93m[ 10 ]\033[0m\n")) 
                self.cart = cart       
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
                    # Chamar o método para criar a nota fiscal em PDF
                    self.criar_nota_fiscal_pdf(total_venda, metodo_pagamento)
            else:
                print(f"\033[92mVenda realizada com sucesso!\033[0m")
                print(f"Pagamento: {metodo_pagamento}")
                # Chamar o método para criar a nota fiscal em PDF
                self.criar_nota_fiscal_pdf(total_venda, metodo_pagamento)

# Função para executar as vendas
def executar_vendas():
    # Conectar ao banco de dados ou criar um novo arquivo de banco de dados se ele não existir
    conn = sqlite3.connect('Database/store.db')
    c = conn.cursor()

    # Criar uma instância da classe Venda
    venda = Venda(conn, c)

    while True:
        produto_id_nome = input("Digite o ID ou o Nome do produto que deseja vender (ou 'não' para encerrar):\n")

        if produto_id_nome.lower() == 'não':
            break

        quantidade_venda = float(input(f"Digite a quantidade de {produto_id_nome} que deseja vender:\n"))

        # Adicionar o produto à lista de produtos da venda
        venda.adicionar_produto(produto_id_nome, quantidade_venda)

    # Realizar a venda apenas no final, após adicionar todos os produtos
    total_venda = venda.realizar_venda()

    # Fechar a conexão com o banco de dados
    conn.close()

#executar_vendas()
