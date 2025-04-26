import os
import pyodbc
from dotenv import load_dotenv


load_dotenv()
server = 'localhost'
database = 'SistemaCadastroTarefa'
username = 'sa'
password = os.getenv("DB_PASS")
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}',
        timeout=5
    )

cursor = conn.cursor()
print("Conectado ao banco com sucesso!")
cursor.execute("INSERT INTO Tarefas (Descricao, Status, DataCriacao) VALUES (?, ?, GETDATE())",('Lavar roupa', 'Não iniciada'))
conn.commit()
cursor.execute("SELECT * FROM Tarefas")
rows = cursor.fetchall()
print("\nTarefas cadastradas:")
for row in rows:
    print(f"ID: {row.TarefaId}, Descrição: {row.Descricao}, Data Criação: {row.DataCriacao}")
