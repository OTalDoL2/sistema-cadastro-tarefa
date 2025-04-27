import os
from dotenv import load_dotenv
import pyodbc

class Database:
    def __init__(self, server, database, username, password, driver):
        self.server = server 
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        
    def estabelecer_conexao(self):
        load_dotenv()
        server = 'localhost'
        database = 'SistemaCadastroTarefa'
        username = 'sa'
        password = os.getenv("DB_PASS")
        driver = '{ODBC Driver 17 for SQL Server}'
        try:
            self.conn = pyodbc.connect(f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}', timeout=5)
            print("Conexão com o banco estabelecida com sucesso!")
        except Exception as e:
            print(f'Falha na conexão. Erro: {e}')
            self.conn = None
            
    def __buscar_status_atual(self, id, cursor):
        cursor.execute("EXEC BuscarStatus ?", (id))
        status_atual = cursor.fetchall()
        return status_atual[0][0]
            
    def adicionar_nova_tarefa(self, descricao):
        cursor = self.conn.cursor()
        cursor.execute("EXEC AdicionarNovaTarefa ?",(descricao))
        self.conn.commit()
        cursor.close()
        print('Tarefa Criada com Sucesso!')
    
    def listar_tarefas(self):
        cursor = self.conn.cursor()
        cursor.execute("EXEC ListarTarefas")
        rows = cursor.fetchall()
        print("\nTarefas cadastradas:")
        for row in rows:
            print(f"ID: {row.TarefaId}, Descrição: {row.Descricao}, Status da Tarefa: {row.Status}, Data Criação: {row.DataCriacao}, Data Conclusão: {row.DataConclusao}")
        cursor.close()
        
    def atualizar_status(self, id):
        cursor = self.conn.cursor()
        status_atual = self.__buscar_status_atual(id, cursor)
        print(status_atual[0][0])
        if status_atual == 'Não Iniciada':
            cursor.execute("EXEC AtualizarStatusTarefa ?, ?", ('Em Andamento', id))
        elif status_atual == 'Em Andamento':
            cursor.execute("EXEC ConcluirTarefa ?", (id))
            
        self.conn.commit()
        cursor.close()
        print('Status atualizado com sucesso!')
        
    def deletar_tarefa(self, id):
        cursor = self.conn.cursor()
        cursor.execute("EXEC DeletarTarefa ?", (id))
        self.conn.commit()
        cursor.close()
    
    def cancelar_tarefa(self, id):
        cursor = self.conn.cursor()
        cursor.execute("EXEC CancelarTarefa ?", (id))
        self.conn.commit()
        cursor.close()

    def encerrar_conexao(self):
        self.conn.close()
        