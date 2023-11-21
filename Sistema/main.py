from Instalar_depedencias import *
setup_ambiente()
# caso não saiba nenhuma senha ou login instale o DB BROWSER FOR SQLITE e abra o banco security na tabela login
from login import Login
login_obj = Login()
login_obj.verificacao()