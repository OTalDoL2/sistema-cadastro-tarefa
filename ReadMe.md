# 📘 Documentação da API - Sistema de Cadastro de Tarefas

## 🔧 Requisitos Iniciais

Antes de iniciar, certifique-se de ter os seguintes itens instalados no seu sistema:

* Python 3.10+
* SQL Server
* Git (opcional, para clonar o repositório)

## 📁 Configuração do Ambiente
### 1. Clone o repositório (se aplicável):

    git clone https://github.com/usuario/repositorio.git
    cd repositorio


### 2. Crie e ative o ambiente virtual

Windows:

    python -m venv venv
    venv\Scripts\activate

Linux/macOS:

    python3 -m venv venv
    source venv/bin/activate

## 📦 Instalação das Dependências
Instale as bibliotecas necessárias com:

    pip install -r requirements.txt

## 🗂️ Configuração do .env

Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

    DB_PASS=sua_senha

Então você deve preencher o DB_PASS com a senha definida ao instalar e definir a senha do SQL Server.

## 🛠️ Preparar o Banco de Dados

Existem alguns scripts SQL, dentro da pasta "sql", você pode executar o arquivo "index.sql" ou executar as queries separadas por aquivo e funcionalidades.

### Para criar o Banco de Dados, executar as queries do arquivo:
    
    Criacao BD.sql

### Para criar Procedures, executar as queries do arquivo:
    
    Procedures.sql

### Para popular o Banco de Dados, executar as queries do arquivo:
    
    Populacao.sql
    
_OBS: para rodar o arquivo de Populacao, é necessário que o script de Procedures seja rodado primeiro._

## 🚀 Rodar a API

Você pode iniciar a API localmente com:

    python index.py
    

## 🌐 Exemplos de Requests
GET - Listar tarefas

    GET /listar-tarefas

GET - Listar tarefa

    GET /listar-tarefa/<int:id>

POST - Adicionar nova tarefa

    POST /adicionar-nova-tarefa
    Content-Type: application/json
    
    {
        "tarefa": "Comprar placa de vídeo"
    }

PUT - Atualizar Status
    
    PUT /atualizar-status/<int:id>
_Você só precisa passar o id da tarefa, automaticamente é feita a progressão dos status. Uma atividade cancelada ou concluída não pode mudar seu status._
_Não iniciada -> Em Andamento -> Concluída_



PUT - Cancelar Tarefa

    PUT cancelar-tarefa/<int:id>
_Uma tarefa não iniciada ou em andamento podem ser canceladas, mantendo o registro para geração do relatório._

DELETE - Deletar Tarefa

    DELETE deletar-tarefa/<int:id>
_Qualquer tarefa que não esteja com o status de "Concluída" pode ser excluída. Tarefas excluídas não aparecerão no relatório._

GET - Gerar Relatório

    GET /gerar-relatorio

