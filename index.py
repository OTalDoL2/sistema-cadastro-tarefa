from Database import Database
from Relatorio import Relatorio
from flask import Flask, request, g

app = Flask(__name__)

@app.route('/adicionar-nova-tarefa', methods=['POST'])
def adicionar_tarefa():
    tarefa = request.get_json()['tarefa']
    g.db.adicionar_nova_tarefa(tarefa)
    return '<h1> Tarefa adicionada com sucesso! </h1>'

@app.route('/listar-tarefas', methods=['GET'])
def listar_tarefas():
    lista_tarefas = g.db.listar_tarefas()
    
    dict_tarefas = {}
    for tarefa in lista_tarefas:
        dict_tarefas[tarefa[0]] = {}
        dict_tarefas[tarefa[0]]['tarefa'] = tarefa[1]
        dict_tarefas[tarefa[0]]['status'] = tarefa[2]
        dict_tarefas[tarefa[0]]['data_inicio'] = tarefa[3]
        dict_tarefas[tarefa[0]]['data_fim'] = tarefa[4]
        
    return dict_tarefas

@app.route('/listar-tarefa/<int:id>', methods=['GET'])
def listar_tarefa(id_tarefa):
    tarefa = g.db.listar_tarefa_pelo_id(id_tarefa)
    
    dict_tarefas = {}
    dict_tarefas[tarefa[0]] = {}
    dict_tarefas[tarefa[0]]['tarefa'] = tarefa[1]
    dict_tarefas[tarefa[0]]['status'] = tarefa[2]
    dict_tarefas[tarefa[0]]['data_inicio'] = tarefa[3]
    dict_tarefas[tarefa[0]]['data_fim'] = tarefa[4]
        
    return dict_tarefas

@app.route('/atualizar-status/<int:id>', methods=['PUT'])
def atualizar_status_tarefa(id):
    g.db.atualizar_status(id)
    return'<h1>Status atualizado com sucesso!</h1>'
    
@app.route('/deletar-tarefa/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    g.db.deletar_tarefa(id)
    return'<h1>Tarefa deletada com sucesso!</h1>'
    
@app.route('/cancelar-tarefa/<int:id>', methods=['PUT'])
def cancelar_tarefa(id):
    g.db.cancelar_tarefa(id)
    return'<h1>Tarefa cancelada com sucesso!</h1>'
    
@app.route('/gerar-relatorio', methods=['GET'])
def gerar_relatorio():
    tarefas = g.db.listar_tarefas()
    relatorio = Relatorio(tarefas)
    relatorio.gerar_relatorio()
    return "<h1>Relatório gerado com sucesso!</h1>"
    
@app.route('/reconectar-db')
def reestabelecer_conexao():
    g.db.estabelecer_conexao()
    
@app.before_request
def conectar_com_banco():
    if 'db' not in g:
        g.db = Database()
        g.db.estabelecer_conexao()
    
@app.route('/')
def index():
    return '<h1>Seja bem vindo ao Sistema de Cadastro de Tarefas!</h1>'

if __name__ == "__main__":
    app.run(debug=True)