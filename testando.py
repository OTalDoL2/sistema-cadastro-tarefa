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

# # create a Canvas object with a filename
c = canvas.Canvas("teste.pdf")
c.setFont("Helvetica-Bold", 12)
c.drawString(542, 810, f"Relatório")
c.drawString(0, 810, f"Relatório")
c = canvas.Canvas("teste.pdf")

logo = colors.HexColor('#036ffc')
cinza_claro = colors.HexColor('#f2f2f2')
preto = colors.black


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


a = 750
c.setFont("Helvetica-Bold", 12)
c.drawString(50, 765, "ID")
c.drawString(150, 765, "Tarefa")
c.drawString(300, 765, "Status")
c.drawString(405, 765, "Data Inicio")
c.drawString(515, 765, "Data Fim")
c.setFont("Helvetica", 10)
# ⚪🔴🟡🟢
for tarefa in tarefas:
    c.drawString(50, a, str(tarefa[0]))
    c.drawString(150, a, str(tarefa[1]))
    c.drawString(312, a, "@")
    c.drawString(410, a, str(tarefa[3]))
    c.drawString(515, a, str(tarefa[4]))
    a -= 20

c.drawString(530, 810, f"Relatório")
c.drawString(0, 810, f"Relatório")

c.setFont("Helvetica", 10)
# c.drawString(50, 780, "Hello Again")
# c.drawString(50, 843, "asdfasdfa Again")
linha(25, 575, 780)
# c.line(10,300,300,300)
    
# logo
# wave = Group(
#     Line(10, -5, 10, 10),
#     Line(20, -15, 20, 20),
#     Line(30, -5, 30, 10),
#     Line(40, -15, 40, 20),
#     Line(50, -5, 50, 10),
#     Line(60, -15, 60, 20),
#     Line(70, -5, 70, 10),
#     Line(80, -15, 80, 20),
#     Line(90, -5, 90, 10),
#     String(25, -25, "Wave Audio", fontName='Times')
# )
# wave.translate(10, 170)
# drawing.add(wave)

c.showPage()
c.save()


# # draw a string at x=100, y=800 points
# # point ~ standard desktop publishing (72 DPI)
# # coordinate system:
# #   y
# #   |
# #   |   page
# #   |
# #   |
# #   0-------x

# # finish page
# # construct and save file to .pdf



