import os
import datetime
#from lib.funcoes import *
from time import sleep

menu_vendas = ["Abrir Caixa", "Sair"]
menu_abrir_caixa = ["Nova Venda","Novo Orçamento","Gestão de Produtos", "Encerrar Caixa"]
gestao_produtos= ["Adicionar Produto", "Remover Produto", "Editar Prduto"]
S_N = ["Sim", "Não"]
tipo_venda = ["Venda Simples", "Venda Avulsa"]

#imprime uma mensagem indicando que a opção informada é inválida
def opcao_invalida():
    print("        OPÇÃO INVÁLIDA!!!")
    print("Verifique as opções e tente novamente")


#Limpa tela e imprime cabeçalho com nome do parametro informado
def nova_tela(nome_cabecalho):
    os.system("cls")
    print("="*38)
    print(f"             {nome_cabecalho}")
    print("="*38)

#Recebe uma lista como parametro e imprime em forma de opções com seus respectivos indices iniciando por 1
#Retorna como a variavel opcao o valor referente ao indice informado pelo usuário de acordo com seu interesse
def imprime_opcoes(lista):
    indice = 0
    for i in lista:
        indice += 1
        print(f"[{indice}] {i}")

    opcao = int(input("Informe a opção desejada:"))
    return opcao

#Abre um novo caixa e informa data e hora da abertura
def abrir_caixa():
    print("Deseja abrir um novo caixa?")
    confima_abertura =  imprime_opcoes(S_N)
    
    if confima_abertura == 1:

        nova_tela("MENU VENDEDOR")
        data_hora = datetime.datetime.now()
        data_hora_str = data_hora.strftime("%d/%m/%Y %H:%M")
        print(f"CAIXA ABERTO {data_hora_str}")
        
        caixa_aberto = True
    


#################################################################
#                         PRINCIPAL
#################################################################

caixa_aberto = False

nova_tela("MENU VENDEDOR")
opcao = imprime_opcoes(menu_vendas)


#Menu principal
if opcao == 1:
    nova_tela("MENU VENDEDOR")       
    abrir_caixa()

    #Painel do vendedor (Vendas, orçamentos, encerrar caixa e sair)
    opcao_2 = imprime_opcoes(menu_abrir_caixa)
    
    #Nova venda
    if opcao_2 == 1:
        nova_venda = "SIM"
        
        while nova_venda == "SIM" or nova_venda == "S":
            nova_tela("Nova Venda")
            t_venda = imprime_opcoes(tipo_venda)
            
            if t_venda == 1:
                nova_tela("Venda Direta")
                print("Produtos Cadastrados")
            
            elif t_venda == 2:
                nova_tela("Venda Avulsa")    
                nome_produto = input("Nome do Produto: ")
                valor = float(input("Valor: "))

                #Necessário implementar uma funçãoa que coloque os produtos
                #vendidos dentro do banco de dados
            
            nova_venda = input("Deseja inserir um novo produto?").strip().upper()

    #Novo Orçamento
    elif opcao_2 == 2:
        print("Novo Orçamento")

    #Encerrar caixa 
    elif opcao_2 == 4:
        print("Encerrar caixa")


elif opcao == 2:
    produtos = imprime_opcoes(gestao_produtos)
    
    if produtos == 1:
        print("Adicionar Produtos")
    elif produtos == 2:
        print("")

elif opcao == 2:
    print("Obrigado por utilizar o Gerentia")

else:
    opcao_invalida()

