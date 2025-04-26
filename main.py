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

db.listar_tarefas()
db.atualizar_status(1, 'Em Andamento')
db.listar_tarefas()