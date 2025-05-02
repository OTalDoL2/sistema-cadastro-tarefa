from Database import Database
from Relatorio import Relatorio

db = Database()
db.estabelecer_conexao()

def break_line(task_text):
    if len(task_text) > 22:
        position = task_text.rfind(' ', 0, 22)
        if position != -1:
            parte1 = task_text[:position]
            parte2 = task_text[position+1:]
            broke_text = [parte1, parte2]
        else:
            broke_text = [task_text[:21], task_text[22:]]
            
    else:
        space = " " * (22- len(task_text))
        broke_text = [task_text + space]

    return broke_text

def process_date(date):
    if date == None:
        return "Não encerrada"
    else:
        return date.strftime("%d/%m/%Y")

def structure_tasks_view(tasks_raw):
    tasks = {
        "id": tasks_raw[0],
        "status": tasks_raw[2],
        "data_inicio": process_date(tasks_raw[3]),
        "data_fim": process_date(tasks_raw[4]),
    }
    
    tasks['tarefa'] = break_line(tasks_raw[1])
    view_text = f"\t\t{tasks['id']}\t\t{tasks['tarefa'][0]}\t\t{tasks['status']}\t\t{tasks['data_inicio']}\t\t{tasks['data_fim']}"
    if len(tasks['tarefa']) > 1:
        view_text += f"\n\t\t\t\t{tasks['tarefa'][1]}"
    return view_text + '\n'

def show_tasks(tasks):
    title = "\n\t\tID\t\t\tTAREFA\t\t\tSTATUS\t\t\tDATA INICIO\t\tDATA FIM\n"
    print(title)
    for i in range(len(tasks)):
        view = structure_tasks_view(tasks[i])
        print(view)
    print('\n\n')

def get_task():
    tasks = db.listar_tarefas()
    show_tasks(tasks)

def add_new_task():
    new_task = input('Digite a tarefa que deseja adicionar: ')
    db.adicionar_nova_tarefa(new_task)
    print('Nova tarefa adicionada com sucesso!')

def update_task_status():
    task_id = int(input('Digite o ID da tarefa que deseja registrar um progresso: '))
    db.atualizar_status(task_id)
    updated_task = db.listar_tarefa_pelo_id(task_id)
    print(f'A tarefa foi atualizada com sucesso!')
    show_tasks(updated_task)
    

def delete_task():
    task_id = input('Digite a tarefa que deseja deletar: ')
    db.deletar_tarefa(task_id)
    print('Tarefa deletada com sucesso!')

def cancel_task():
    task_id = input('Digite a tarefa que deseja cancelar: ')
    db.cancelar_tarefa(task_id)
    print('Tarefa cancelada com sucesso!')
    

def report_generate():
    tarefas = db.listar_tarefas()
    relatorio = Relatorio(tarefas)
    relatorio.gerar_relatorio()

def switch_choice(selected_option):
        
    if selected_option == '0':
        pass
    elif selected_option == '1':
        get_task()
    elif selected_option == '2':
        add_new_task()
    elif selected_option == '3':
        update_task_status()
    elif selected_option == '4':
        cancel_task()
    elif selected_option == '5':
        delete_task()
    elif selected_option == '6':
        report_generate()
    else:
        print('opção inválida! Digite novamente.\n\n')

if '__main__' in __name__:
    ativo = 1
    while ativo == 1:
        print('Seja bem vindo ao Sistema de Cadastro de Tarefas')
        print('para melhor funcionamento, é recomendado que utilize o terminal em tela cheia\n')
        print('Pressione as teclas conforme desejar realizar as operações.')
        print('1 - Listar todas as tarefas')
        print('2 - adicionar nova tarefa')
        print('3 - atualizar status de tarefa')
        print('4 - cancelar tarefa')
        print('5 - deletar tarefa')
        print('6 - gerar relatório')
        print('0 - Encerrar a aplicação')
        selected_option = input('Desejo a opção: ')
        
        if selected_option == '0':
            ativo = 0
            
        switch_choice(selected_option)
    
    print('Obrigado por testar.')


# db.atualizar_status(1, 'Em Andamento')
db.listar_tarefas()
# db.adicionar_nova_tarefa('Cozinha batata')
db.listar_tarefas()
db.atualizar_status(2)
db.listar_tarefas()
db.atualizar_status(2)
# db.deletar_tarefa(1)
db.listar_tarefas()