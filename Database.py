import pyodbc

class Database:
    def __init__(self, server, database, username, password, driver):
        self.server = server 
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        
    def estabelecer_conexao(self):
        try:
            self.conn = pyodbc.connect(f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}', timeout=5)
            print("Conexão com o banco estabelecida com sucesso!")
        except Exception as e:
            print(f'Falha na conexão. Erro: {e}')
            self.conn = None
            
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
        
    def atualizar_status(self, id, novo_status="Desconhecido"):
        cursor = self.conn.cursor()
        if novo_status == "Desconhecido":
            cursor.execute("EXEC BuscarStatus ?", (id))
            
        if novo_status == 'Concluído':
            cursor.execute("EXEC ConcluirTarefa ?", (id))
            print('Parabéns, tarefa concluída com sucesso!')
        else:
            cursor.execute("EXEC AtualizarStatusTarefa ?, ?", (novo_status, id))
        self.conn.commit()
        cursor.close()
        print('Tarefa Criada com Sucesso!')
        
    def deletar_tarefa(self, id):
        cursor = self.conn.cursor()
        cursor.execute("EXEC DeletarTarefa ?", (id))
        self.conn.commit()
        cursor.close()
    
    def encerrar_conexao(self):
        self.conn.close()
        
        
        
    

# cursor = conn.cursor()
# print("Conectado ao banco com sucesso!")
# cursor.execute("INSERT INTO Tarefas (Descricao, Status, DataCriacao) VALUES (?, ?, GETDATE())",('Lavar roupa', 'Não iniciada'))
# conn.commit()