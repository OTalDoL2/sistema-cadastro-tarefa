from reportlab.pdfgen import canvas
import reportlab.lib.colors as colors

logo = colors.HexColor('#036ffc')
verde = colors.HexColor('#04b309')
amarelo = colors.HexColor('#fce703')
vermelho = colors.HexColor('#c70421')
cinza = colors.HexColor('#bfb8b9')
cinza_claro = colors.HexColor('#f2f2f2')
preto = colors.black

class Relatorio:
    def __init__(self, tarefas):
        self.tarefas = tarefas
        self.c = canvas.Canvas("teste_oficial.pdf")
        self.c.setFont("Helvetica-Bold", 12)
    
    def gerar_relatorio(self):
        tarefas_separadas_pagina = [self.tarefas[i:i+32] for i in range(0, len(self.tarefas), 32)]
        quantidade_paginas = len(tarefas_separadas_pagina)
        
        for i in range(quantidade_paginas):
            self.__cabecalho()
            self.__lista_itens(tarefas_separadas_pagina[i])
            
            if quantidade_paginas > 1 and quantidade_paginas - i != 1:
                self.c.showPage()
        self.c.save()
        
    def __cabecalho(self):
        self.c.setFont("Helvetica-Bold", 15)
        self.c.setFillColor(preto)

        self.c.drawString(162, 820, f"Sistema de Monitoramento de Tarefas")
        self.c.drawString(35, 785, "Relatório")

        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(35, 765, "ID")
        self.c.drawString(80, 765, "Tarefa")
        self.c.drawString(315, 765, "Status")
        self.c.drawString(405, 765, "Data Inicio")
        self.c.drawString(515, 765, "Data Fim")
        self.c.setFont("Helvetica", 10)

    def __status_tratado(self, status):
        if status == 'Cancelada':
            return vermelho
        elif status == 'Não Iniciada':
            return cinza
        elif status == 'Concluída':
            return verde
        else:
            return amarelo
           
    def __adicionando_status(self, x, y, status):
        self.c.setFillColor(self.__status_tratado(status))
        self.c.circle(x, y, 5, fill=1)
        self.c.setFillColor(preto)
        
    def __data_tratada(self, data):
        if data == None:
            return "Não encerrada"
        else:
            return data.strftime("%d/%m/%Y")
    
    def __lista_itens(self, tarefas):
        altura = 750

        for tarefa in tarefas:
            self.c.drawString(35, altura, str(tarefa[0]))
            self.c.drawString(80, altura, str(tarefa[1]))
            self.__adicionando_status(333, altura, tarefa[2])
            self.c.drawString(410, altura, self.__data_tratada(tarefa[3]))
            self.c.drawString(515, altura, self.__data_tratada(tarefa[4]))
            altura -= 20