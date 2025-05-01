from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Database import Database

from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import reportlab.lib.colors as colors

db = Database()
db.estabelecer_conexao()
tarefas = db.listar_tarefas()
print('a',len(tarefas))
print(tarefas)



def linha(inicio, fim, altura):
    c.line(inicio,altura,fim,altura)

def coluna(inicio, fim, altura):
    c.line(altura,inicio,altura,fim)

c = canvas.Canvas("teste.pdf")
c.setFont("Helvetica-Bold", 12)
c.drawString(542, 810, f"Relatório")
c.drawString(0, 810, f"Relatório")
c = canvas.Canvas("teste.pdf")

logo = colors.HexColor('#036ffc')
verde = colors.HexColor('#04b309')
amarelo = colors.HexColor('#fce703')
vermelho = colors.HexColor('#c70421')
cinza = colors.HexColor('#bfb8b9')
cinza_claro = colors.HexColor('#f2f2f2')
preto = colors.black


    

paginas = [tarefas[i:i+32] for i in range(0, len(tarefas), 32)]

for i in range(len(paginas)):
    c.setFont("Helvetica-Bold", 15)

    c.setFillColor(logo)
    c.drawString(550, 10, f"SMT")

    c.setFillColor(cinza_claro)
    c.drawString(551, 11, f"SMT")

    c.setFillColor(preto)



    c.setFont("Helvetica-Bold", 15)
    c.drawString(162, 820, f"Sistema de Monitoramento de Tarefas")
    # c.drawString(265, 790, f"Relatório")
    c.drawString(35, 785, "Relatório")


    c.setFont("Helvetica-Bold", 12)
    c.drawString(35, 765, "ID")
    c.drawString(80, 765, "Tarefa")
    c.drawString(315, 765, "Status")
    c.drawString(405, 765, "Data Inicio")
    c.drawString(515, 765, "Data Fim")
    c.setFont("Helvetica", 10)
    
    def trata(status_primario):
        print(status_primario)
        if status_primario == 'Cancelada':
            return vermelho
        elif status_primario == 'Não Iniciada':
            return cinza
        elif status_primario == 'Concluída':
            return verde
        else:
            return amarelo

    pagina = paginas[i]
    a = 750

    for tarefa in paginas[i]:
        c.drawString(35, a, str(tarefa[0]))
        c.drawString(80, a, str(tarefa[1]))
        c.setFillColor(trata(tarefa[2]))
        c.circle(333, a, 5, fill=1)
        c.setFillColor(preto)
        c.drawString(410, a, str(tarefa[3]))
        c.drawString(515, a, str(tarefa[4]))
        a -= 20
        
    if len(paginas ) > 1 and len(paginas) - i != 1:
        c.showPage()

c.save()
