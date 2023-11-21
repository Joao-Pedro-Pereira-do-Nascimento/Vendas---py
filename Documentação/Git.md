# Como usar?
Abra o Terminal no VSCode:
No VSCode, vá para "Terminal" no menu superior e escolha "Novo Terminal". Isso abrirá um terminal integrado no VSCode.

Navegue até o diretório do seu projeto:
Use o comando cd para navegar até o diretório onde está o seu projeto local.

Exemplo:

bash

cd caminho/do/seu/projeto

Inicie o repositório Git:
Se o seu projeto ainda não estiver sendo rastreado pelo Git, você pode inicializá-lo com o comando:

csharp

#git init

Adicione os arquivos ao commit:
Use o comando git add para adicionar os arquivos que você deseja ao próximo commit. Você pode adicionar todos os arquivos com:

csharp

#git add .

Ou pode adicionar arquivos individualmente, substituindo . pelo nome do arquivo.

Faça um commit:
Após adicionar os arquivos, você precisa fazer um commit para confirmar as alterações. Use o comando git commit:

sql

#git commit -m "Mensagem do commit"

Substitua "Mensagem do commit" por uma descrição significativa do que foi alterado no commit.

Conecte o repositório remoto do GitHub:
Para conectar o seu repositório local ao repositório remoto no GitHub, use o comando:

csharp

#git remote add origin https://github.com/Alesh-Silva/Project-Vendas.git
Caso não de certoj
#git remote set-url origin https://github.com/Alesh-Silva/Project-Vendas.git


Substitua seu-usuario pelo seu nome de usuário no GitHub e seu-repositorio pelo nome do seu repositório.

Envie as alterações para o GitHub:
Use o comando git push para enviar as alterações para o GitHub:

perl

    #git push -u origin master

    Isso envia as alterações para a branch principal (master). Se você estiver usando outra branch, substitua master pelo nome da sua branch.

Agora, seu código deve estar no GitHub. Você pode verificar acessando o seu repositório no GitHub.

Lembrando que esses são os passos básicos para fazer o deploy de um repositório no GitHub usando o terminal do VSCode. Certifique-se de adaptar esses comandos às suas necessidades específicas e às configurações do seu projeto.
### 📋 Pré-requisitos
Necessário git está instalado
