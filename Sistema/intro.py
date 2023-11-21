from time import sleep
from os import system
def iniciar_intro():
    string = "PROJECT VENDAS - GERENTIA "
    amarelo = '\033[1;33m'; tag = '\033[m'

    def efeito_digitacao(mensagem):
        for char in mensagem:
            sleep(0.05)
            print(char, end='', flush=True)
        print()


    def mostrar_logo(nome, cor):
        print(f"""{cor}
    \t\t                    &                   
    \t\t                    &                   
    \t\t           &        &        &          
    \t\t            &               &           
    \t\t    &&         &&&&   &&&&         &&   
    \t\t       &&   &&      &&&&&  &&   &&      
    \t\t           &              &  &          
    \t\t          &&               & &&         
    \t\t          &&                 &&         
    \t\t           &                 &          {tag}{nome}{cor}
    \t\t            &&             &&           
    \t\t              &&         &&             
    \t\t               &         &              
    \t\t               {tag}\033[36m                 
    \t\t               &&&&&&&&&&&              
    \t\t                &&&&&&&&&
    \t\t{tag}""")
    

    ###usando system cls
    for i in range(0, len(string)): #escrevendo nome
        mostrar_logo(string[0:i], amarelo)
        if string[i] != ' ':
            sleep(0.1)
        else:
            sleep(0.35)
        system("cls||clear")
    for i in range(len(string)-1, string.index(' '), -1): #apagando nome
        mostrar_logo(string[0:i], amarelo)
        sleep(0.1)
        system("cls||clear")
    for i in range(string.index(' '), 0, -1):
        mostrar_logo(string[0:i], amarelo)
        sleep(0.35)
        system("cls||clear")

    efeito_digitacao("Bem-vindo ao PROJECT VENDAS - GERENTIA!")
    sleep(3)
    system("clear||cls")
