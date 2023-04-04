
# LOJA - IMPORTAÇAO CSV
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/Duarts-D/loja-importacao_csv/blob/master/licence)

# Sobre o projeto
A loja - importaçao csv e uma aplicaçao feito em python e django.

A aplicaçao consiste em fazer upload de arquivo tipo csv , onde os dados sao coletados e verificados ,  se contem erros sao retornados para o usuario ,  conforme tudo for bem sucedido sera salvo no banco de dados, assim redirecionando o cliente  para uma lista de invetario ,onde ele podera verifica uma lista dos arquivo importados.

A aplicaçao consiste em um sistema de upload de atualizaçao em arquivo salvo no sistema, atualizando somente quantidade e preço, se os demais campos coincidirem em um produto.

# Layout web
![web 1](https://github.com/Duarts-D/loja-importacao_csv/blob/master/img/inventario.PNG)

![web 2](https://github.com/Duarts-D/loja-importacao_csv/blob/master/img/importacao.PNG)


# Tecnologias utilizadas


# black and
- Python
- Django
- Pandas
- Django-filter
- Factory-boy
- Pytest
- Pytest-cov

# frond end web
- HTML / CSS / JS 
- Bootstrap
## Como execultar o projeto

```bash
# clonar repositório
git clone https://github.com/Duarts-D/loja-importacao_csv.git

# Versao Python 3.10.10
Para roda o programa sem ocorrer travamentos, necessario
python 3.10.10

# Criar ambiente virtual
Windows - python -m venv venv
linux - python3 -m venv venv

# Ativando ambiente virtual
Windows - .\venv\Scripts\Activate.ps1
linux - source venv\bin\activate

# instalar dependências
pip install -r requeriments.txt

# rodando migraçoes
windows - python manage.py makemigrations
windows - python manage.py migrate

linux - python3 manage.py makemigrations
linux - python3 manage.py migrate

# executar o projeto
windows - python manage.py runserver
linux - python3 manage.py runserver
```

