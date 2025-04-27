import os
from dotenv import load_dotenv
from Database import Database

load_dotenv()
server = 'localhost'
database = 'SistemaCadastroTarefa'
username = 'sa'
password = os.getenv("DB_PASS")
driver = '{ODBC Driver 17 for SQL Server}'

db = Database(server, database, username, password, driver)
db.estabelecer_conexao()

# db.atualizar_status(1, 'Em Andamento')
db.listar_tarefas()
# db.adicionar_nova_tarefa('Cozinha batata')
db.listar_tarefas()
db.atualizar_status(2)
db.listar_tarefas()
db.atualizar_status(2)
# db.deletar_tarefa(1)
db.listar_tarefas()