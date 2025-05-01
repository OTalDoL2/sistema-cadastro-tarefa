from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import reportlab.lib.colors as colors
import pandas as pd

class Relatorio:
    bege = colors.HexColor('#fff2cc')
    verde = colors.HexColor('#70ad47')
    logo = colors.HexColor('#036ffc')
    cinza_claro = colors.HexColor('#f2f2f2')
    cinza_medio = colors.HexColor('#d9d9d9')
    cinza_escuro = colors.HexColor('#aeaaaa')
    
    def __init__(self):
        pass
    
    

def titulo(c, estado_selecionado):
    c.setFont("Helvetica-Bold", 11)
    c.drawString(120, 745, f"Classificação da Cobertura da Terra do Estado de {estado_selecionado}")


def descricao(c, texto):
    c.setFont("Helvetica", 10)
    paragrafos(c, texto, 56, 350, 1, 'justify')

    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, 415, "1. Descrição")

def tabela(c, level):
    base_x = 200

    c.setFont("Helvetica", 11)
    c.drawString(base_x, 330, "Tabela 1 - Classes de Cobertura da Terra")
    dados_tabela_classes = coleta_dados_tabela(level)
    template_atributos_tabela(c, 200, level, dados_tabela_classes)
    gera_grid_tabela(c, 200, level)

def fonte_dados(c, altura):
    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, altura + 15, "2. Fonte de Dados")

    c.setFont("Helvetica", 10)
    c.drawString(56, altura, "Vega Monitoramento")

def escala(c, altura):
    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, altura + 15, "3. Escala")

    c.setFont("Helvetica", 10)
    c.drawString(56, altura, "1:50.000")

def pagina_anexos(c, level, estado_selecionado):
    estado = estado_selecionado['Estado'].loc[0]
    sigla = estado_selecionado['Sigla'].loc[0]

    if level == 1:
        altura = 650
    else:
        altura = 450
    c.drawImage(f'./arquivos_relatorio/imagens/landcover/Mapa_PontosReferencia_LandCover_{sigla}_Level{level}_2023.jpg', 116, altura - 770, width=375, preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica", 10)
    c.drawString(56, altura, "I - Distribuição dos pontos de referência")

    c.setFont("Helvetica", 9)
    texto = f"Figura 2. Mapa de Cobertura da Terra do Estado de {estado} com a distribuição dos pontos de referência."
    c.drawString(90, altura - 300, texto)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, altura + 20, "Anexos")

def extensao_territorial(c, altura, coords):
    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, altura, "4. Extensão Espacial")

    c.setFont("Helvetica", 10)
    c.drawString(56, altura - 15, f"Latitude mínima:  {coords[0]}") # -12.394973
    c.drawString(56, altura - 25, f"Latitude máxima:  {coords[1]}") # -19.498364
    c.drawString(56, altura - 35, f"Longitude mínima: {coords[2]}") # -45.907155
    c.drawString(56, altura - 45, f"Longitude máxima: {coords[3]}") # -53.248562

def sistema_coordenadas(c, altura):
    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, altura, "5. Sistema de Coordenadas de Referência")

    c.setFont("Helvetica", 10)
    c.drawString(56, altura - 15, "Sistema de Coordenadas Geográficas Sirgas 2000")

def metodologia(c, altura, data):
    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, altura, "6. Metodologia")

    c.setFont("Helvetica", 10)
    metodologia_texto_1 = "O mapa foi gerado com a utilização de imagens de satélite Sentinel-2, classificadas e processadas usando algoritmos de aprendizado de máquina para identificar e classificar os diferentes tipos de cobertura da Terra."
    paragrafos(c, metodologia_texto_1, 56, altura - 40, 1, 'justify')

    c.drawString(56, altura - 60, f"Período das imagens: {data[0]} a {data[1]}  com cobertura de nuvem de 20%.")

    metodologia_texto_2 = "Coleta de amostras: realizada por interpretação visual de áreas correspondentes às classes de cobertura da terra definidas."
    paragrafos(c, metodologia_texto_2, 56, altura - 95, 1, 'justify')

    metodologia_texto_3 = "Treinamento do Modelo e classificação: as ferramentas empregadas são integralmente disponibilizadas no software ArcGIS Pro e incluem as funcionalidades-chave 'Export Training Data For Deep Learning', 'Train Deep Learning Model' e 'Classify Pixels Using Deep Learning'. Essa abrangente coleção de ferramentas viabiliza a extração de amostras por meio de um dataset que compreende imagens segmentadas, destinadas ao treinamento do modelo. Uma vez concluído o treinamento e efetuada a avaliação preliminar dos resultados, o modelo validado se torna apto a categorizar de maneira precisa todas as imagens de satélite pertinentes à região de interesse."
    paragrafos(c, metodologia_texto_3, 56, altura - 188, 1, 'justify')

    metodologia_texto_4 = "Validação: distribuição aleatória de pontos de referência no mapa classificado e criação de uma matriz de confusão através da comparação das classes associadas a estes pontos com a interpretação visual, resultando na acurácia e coeficiente kappa do mapa."
    paragrafos(c, metodologia_texto_4, 56, altura - 235, 1, 'justify')

def formato_arquivo(c, altura):
    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, altura, "7. Formato do Arquivo")

    c.setFont("Helvetica", 10)
    c.drawString(56, altura - 15, "Raster.tif")

def classifica_agrupamento_qualitativo_kappa(coeficiente_kappa):
    if coeficiente_kappa < 0:
        return "péssimo"
    elif coeficiente_kappa <= 0.2:
        return "ruim"
    elif coeficiente_kappa <= 0.4:
        return "razoável"
    elif coeficiente_kappa <= 0.6:
        return "bom"
    elif coeficiente_kappa <= 0.8:
        return "muito bom"
    elif coeficiente_kappa <= 1:
        return "excelente"



def resultados_validacao(c, altura, tipo_level, estado):
    valor = pd.read_excel(f"./arquivos_relatorio/planilhas_acuracia/Acuracia_{estado}_Level{tipo_level}.xlsx")

    print(valor.columns)
    print(valor)
    print(valor['U_Accuracy'].iloc[-2])
    print(valor['Kappa'].iloc[-1])

    valor_acuracia = round(float(valor['U_Accuracy'].iloc[-2].replace(',', '.')), 2) * 100
    valor_acuracia = int(valor_acuracia)
    coeficiente_kappa = round(float(valor['Kappa'].iloc[-1].replace(',', '.')), 2)

    agrupamento_qualitativo_kappa = classifica_agrupamento_qualitativo_kappa(coeficiente_kappa)



    c.setFont("Helvetica-Bold", 11)
    c.drawString(56, altura, "8. Resultados da Validação")

    c.setFont("Helvetica", 10)



    # if tipo_level == 1:
    #     metodologia_texto_5 = f"Os resultados gerados pela matriz de confusão conforme a tabela 2, apontam que o modelo de classificação possui acurácia global de {valor_acuracia}% e coeficiente Kappa de 0.73, considerado muito bom segundo o agrupamento qualitativo proposto por Fonseca (2000)¹."
    # elif tipo_level == 2:
    #     metodologia_texto_5 = f"Os resultados gerados pela matriz de confusão conforme a tabela 2, apontam que o modelo de classificação possui acurácia global de 80% e coeficiente Kappa de 0.74, considerado muito bom segundo o agrupamento qualitativo proposto por Fonseca (2000)¹."
    # else:
    #     metodologia_texto_5 = f"Os resultados gerados pela matriz de confusão conforme a tabela 2, apontam que o modelo de classificação possui acurácia global de 80% e coeficiente Kappa de 0.74, considerado muito bom segundo o agrupamento qualitativo proposto por Fonseca (2000)¹."
    metodologia_texto_5 = f"Os resultados gerados pela matriz de confusão conforme a tabela 2, apontam que o modelo de classificação possui acurácia global de {valor_acuracia}% e coeficiente Kappa de {coeficiente_kappa}, considerado {agrupamento_qualitativo_kappa} segundo o agrupamento qualitativo proposto por Fonseca (2000)¹."


    paragrafos(c, metodologia_texto_5, 56, altura - 45, 1, 'justify')

    c.setFont("Helvetica", 7)
    c.drawString(45, 32, "¹FONSECA, L. M. G. Processamento digital de imagens. Instituto Nacional de Pesquisas Espaciais (INPE), 2000. 105p.")

def tabela_matriz_confusao(c, altura, level):
    c.setFont("Helvetica", 11)
    if level == 1:
        c.drawString(240, altura + 220, "Tabela 2 - Matriz de Confusão")
        c.drawImage(f'./arquivos_relatorio/imagens/assets_pdf/matriz_confusao_level{level}.png', 50, altura, width=480, preserveAspectRatio=True, mask='auto')
    else:
        c.drawString(240, altura + 230, "Tabela 2 - Matriz de Confusão")
        c.drawImage(f'./arquivos_relatorio/imagens/assets_pdf/matriz_confusao_level{level}.png', 50, altura - 45, width=480, preserveAspectRatio=True, mask='auto')


def coleta_dados_tabela(level_selecionado):

    gridcode_level_1 = [ "10", "20", "30", "50", "60"]
    conteudo_level_1 = [ "Corpos d'água", "Vegetação nativa", "Agropecuária", "Área não vegetada", "Área construída"]

    # gridcode_level_2 = ["10", "21", "31", "32", "36", "37", "50", "60"]
    # conteudo_level_2 = [ "Corpos d'água", "Vegetação nativa", "Pastagem", "Agricultura temporária", "Silvicultura", "Agricultura semiperene e perene", "Área não vegetada", "Área construída" ]
    gridcode_level_2 = ["10", "21", "31", "32", "36", "37", "50", "60"]
    conteudo_level_2 = [ "Corpos d’água", "Vegetação nativa", "Pastagem", "Agricultura temporária", "Silvicultura", "Agricultura semiperene", "Área não vegetada", "Área construída"]

 # gridcode_level_3 = ["10", "21", "31", "32", "33", "34", "36", "53", "60"]
    # conteudo_level_3 = ["Corpos d'gua", "Vegetação nativa", "Pastagem", "Agricultura temporária", "Agricultura semiperene", "Agricultura perene", "Silvicultura", "Solo exposto", "Área construída"]

    gridcode_level_3 = ["10","21","31","32","33","36","52","60"]
    conteudo_level_3 = ["Corpos d’água", "Vegetação nativa", "Pastagem", "Agricultura temporária", "Agricultura semiperene", "Silvicultura", "Solo exposto", "Área construída"]
    # gridcode_level_3 = ["10","21","31","32","33","36","52","53","60"]
    # conteudo_level_3 = ["Corpos d’água", "Vegetação nativa", "Pastagem", "Agricultura temporária", "Agricultura semiperene", "Silvicultura", "Afloramento rochoso", "Solo exposto", "Área construída"]

































    if level_selecionado == 1:
         grid_code_selecionado = gridcode_level_1
         classe_selecionada = conteudo_level_1
    elif level_selecionado == 2:
         grid_code_selecionado = gridcode_level_2
         classe_selecionada = conteudo_level_2
    else:
         grid_code_selecionado = gridcode_level_3
         classe_selecionada = conteudo_level_3

    atributos_tabela_classes = {"Classe": classe_selecionada, "Gridcode": grid_code_selecionado}

    return atributos_tabela_classes

def template_atributos_tabela(c, base_x, level_selecionado, dados_tabela_classes):
    alt_inicial = 310
    c.setFont("Helvetica", 11)
    if level_selecionado == 2:
        base_x -= 46
        c.drawString(base_x + 150, alt_inicial, "Classe")
        c.drawString(base_x + 4, alt_inicial, "Gridcode")
    elif level_selecionado == 1:
        base_x += 20
        c.drawString(base_x + 4, alt_inicial, "Gridcode")
        c.drawString(base_x + 85, alt_inicial, "Classe")
    else:
        c.drawString(base_x + 110, alt_inicial, "Classe")
        c.drawString(base_x + 4, alt_inicial, "Gridcode")



    for i in range(len(dados_tabela_classes['Classe'])):
        c.drawString(base_x + 20, alt_inicial - 18 * (i + 1), dados_tabela_classes['Gridcode'][i])
        c.drawString(base_x + 64, alt_inicial - 18 * (i + 1), dados_tabela_classes['Classe'][i])

def gera_grid_tabela(c, init_x, level_selecionado):
    init_y = 322.5
    if level_selecionado == 3:
        end_x = init_x + 236
        end_y = init_y - 18 * (9)

        # Colunas
        c.line(init_x + 60, init_y, init_x + 60, end_y)
        c.line(init_x, init_y, init_x, end_y)
        c.line(end_x, init_y, end_x, end_y)


        #Linhas
        for i in range(9):
            c.line(init_x, init_y - 18 * i, end_x, init_y - 18 * i)
            c.line(init_x, init_y - 18 * (i + 1), end_x, init_y - 18 * (i + 1))


    elif level_selecionado == 2:
        init_x -= 50
        end_x = init_x + 310
        end_y = init_y - 18 * (9)

        # Colunas
        c.line(init_x + 60, init_y, init_x + 60, end_y)
        c.line(init_x, init_y, init_x, end_y)
        c.line(end_x, init_y, end_x, end_y)

        #Linhas
        for i in range(9):
            c.line(init_x, init_y - 18 * i, end_x, init_y - 18 * i)
            c.line(init_x, init_y - 18 * (i + 1), end_x, init_y - 18 * (i + 1))

    else:
        init_x += 20
        end_x = init_x + 175
        end_y = 196
        end_y = init_y - 18 * (6)

        # Colunas
        c.line(init_x + 56, init_y, init_x + 56, end_y)
        c.line(init_x, init_y, init_x, end_y)
        c.line(end_x, init_y, end_x, end_y)

        #Linhas
        for i in range(6):
            c.line(init_x, init_y - 18 * i, end_x, init_y - 18 * i)
            c.line(init_x, init_y - 18 * (i + 1), end_x, init_y - 18 * (i + 1))

def imagens_fundo(c):
    c.drawImage('./arquivos_relatorio/imagens/assets_pdf/barra_lateral.png', 0, -749, width=28.5, preserveAspectRatio=True, mask='auto')
    c.drawImage('./arquivos_relatorio/imagens/assets_pdf/Logo Vega.png', 45, 665, width=160, preserveAspectRatio=True, mask='auto')
    c.drawImage('./arquivos_relatorio/imagens/assets_pdf/site vega.png', 400, 785, width=165, preserveAspectRatio=True, mask='auto')

def paragrafos(c, texto, x, y, tipo, orientacao):
    valor_orientacao = 0
    if orientacao.lower() == "center" or orientacao.lower() == "centro":
        valor_orientacao = 1
    elif orientacao.lower() == "right" or orientacao.lower() == "direita":
        valor_orientacao = 2
    elif orientacao.lower() == "justify" or orientacao.lower() == "justificado":
        valor_orientacao = 4

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.alignment = valor_orientacao
    paragrafo = Paragraph(texto, style)
    if tipo == 1:
        paragrafo.wrapOn(c, 470, 100)
    else:
        paragrafo.wrapOn(c, 300, 100)
    paragrafo.drawOn(c, x, y)


def paragrafo_matriz_confusao(c, texto, x, y, size):

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.alignment = 1
    style.leading = 6
    style.fontSize = 5
    paragrafo = Paragraph(texto, style)

    paragrafo.wrapOn(c, size, 50)
    paragrafo.drawOn(c, x, y)


def calculate_max_y(df, level):
    const_variacao_y = 9
    y_max = 4 + const_variacao_y * 0
    for i in range(len(df)):
        if i == 2:
            const_variacao_y = 8

        y_max = 4 + const_variacao_y * i

    if level == 2:
        y_max += 12
    return y_max + 2


def detalhes_tabela(c, largura_total, altura_total):
    c.line(23, 10, largura_total - (23 + 3), 10)
    c.line(largura_total - (23 + 3), 10, largura_total - (23 + 3), altura_total - 18)

    c.line(23, 18.5, largura_total - (23 + 38), 18)
    c.line(largura_total - (23 + 38), 18.5, largura_total - (23 + 38), altura_total - 18.5)

    c.line(23, 27, largura_total - (23 + 61), 27)
    c.line(largura_total - (23 + 61), 27, largura_total - (23 + 61), altura_total - 18.5)


def plot_background_colors(c, y, largura_total, largura_variavel, altura_total, altura_variavel):
    bege = colors.HexColor('#fff2cc')
    verde = colors.HexColor('#70ad47')
    cinza_claro = colors.HexColor('#f2f2f2')
    cinza_medio = colors.HexColor('#d9d9d9')
    cinza_escuro = colors.HexColor('#aeaaaa')
    preto = colors.black


    # Tabela
    largura_tabela = largura_variavel * 2 + 21
    altura_tabela = y + 22

    c.setLineWidth(0.5)
    c.setStrokeColor(preto)
    c.setFillColor(cinza_claro)

    c.rect(23, 0, largura_tabela, altura_tabela, fill=1)


    # Titulo Tabela - "Table Confusion Matrix - ArcGIS"
    largura_titulo_tabela = largura_variavel * 2 + 21
    altura_titulo_tabela = 18

    c.setLineWidth(0.5)
    c.setStrokeColor(preto)
    c.setFillColor(verde)

    c.rect(23, y + 22, largura_titulo_tabela, altura_titulo_tabela, fill=1)


    # Célula Classified
    largura_classified = 22.5
    altura_classified = (altura_total - 18) / 2

    c.setLineWidth(0.5)
    c.setStrokeColor(bege)
    c.setFillColor(bege)

    c.rect(0, altura_total/4, largura_classified, altura_classified, fill=1)


    # Posição do ClassValue e ClassName
    largura_classes = 106
    altura_classes = 16.5

    c.setLineWidth(0.5)
    c.setStrokeColor(cinza_medio)
    c.setFillColor(cinza_medio)

    c.rect(23.5, y + 5, largura_classes, altura_classes, fill=1)


    # Célula "GrndTruth"
    largura_grnd = largura_variavel - 10

    c.setLineWidth(0.5)
    c.setStrokeColor(bege)
    c.setFillColor(bege)

    c.rect(130, y + 16.5, largura_grnd, 5, fill=1)


    # Coluna/Linha Total Values
    # largura_coluna_total
    altura_coluna_total = altura_variavel + 9 + 15.5
    largura_linha_total = 119.5 + largura_variavel

    largura_coluna_total = -1 * (largura_variavel - largura_linha_total) / 5

    c.setLineWidth(0.5)
    c.setStrokeColor(cinza_escuro)
    c.setFillColor(cinza_escuro)

    c.rect(23.5, 18, largura_linha_total, 9, fill=1)
    c.rect(largura_linha_total, 18, largura_coluna_total, altura_coluna_total, fill=1)


    # Altura e Coluna Kappa
    largura_coluna_total = 119.5 + largura_variavel

    largura_linha_kappa = largura_total - largura_classified - 1.5
    largura_coluna_kappa = 1.5 + -1 * (largura_variavel - largura_coluna_total) / 5
    altura_coluna_kappa = altura_variavel + 18 + 16.5



    c.setLineWidth(0.5)
    c.setStrokeColor(cinza_medio)
    c.setFillColor(cinza_medio)

    c.rect(23.5, 0.5, largura_linha_kappa + 0.5, 9, fill=1)
    c.rect(largura_linha_kappa - 1.5, 8, largura_coluna_kappa, altura_coluna_kappa, fill=1)

    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)

    detalhes_tabela(c, largura_total, altura_total)


def plot_title(c, altura_inicial, largura, altura):
    c.setFont("Helvetica-Bold", 10, 45)
    c.drawString(int(largura / 3), altura_inicial + 27, "Table Confusion Matrix - ArcGIS", )

    c.setFont("Helvetica-Bold", 5)
    c.drawString(int(largura / 2), altura_inicial + 17, "GrndTruth", )

    c.setFont("Helvetica-Bold", 5.5)


    c.rotate(90)
    c.drawString(altura / 3, -15, "Classified")
    c.rotate(-90)


def converter_para_inteiro_se_necessario(valor):
    # Verifica se o valor já é um inteiro ou tem casas decimais diferentes de zero
    if valor.is_integer():
        return int(valor)  # Se já for um inteiro, retorna o valor convertido
    else:
        return round(valor, 2)  # Se tiver casas decimais diferentes de zero, retorna o valor original




def plot_table(c, level, df, altura_inicial, colunas_confusao):
    c.setFont("Helvetica-Bold", 5.5)
    eixo_x = 136
    eixo_xx = eixo_x

    altura_inicial = altura_inicial - 2
    if level == 2:
        altura_inicial -= 5
    const_variacao_y = altura_inicial

    # print(df[colunas_confusao[0]])
    for i in range(len(colunas_confusao)):
        for j in range(len(colunas_confusao)):
            if 'str' in str(type(df[colunas_confusao[i]].iloc[j])):
                resultado = converter_para_inteiro_se_necessario(float(df[colunas_confusao[i]].iloc[j].replace(',','.')))

                c.drawString(eixo_xx, const_variacao_y, str(resultado))
                # c.drawString(eixo_xx, const_variacao_y, str(round(float(df[colunas_confusao[i]].iloc[j].replace(',','.')), 2)))


            elif 'float' in str(type(df[colunas_confusao[i]].iloc[j])):
                resultado = converter_para_inteiro_se_necessario(df[colunas_confusao[i]].iloc[j])
                c.drawString(eixo_xx, const_variacao_y, str(resultado))

            else:
                c.drawString(eixo_xx, const_variacao_y, str(df[colunas_confusao[i]].iloc[j]))

            if df['ClassValue'].iloc[j] == 'C_37':
                const_variacao_y = const_variacao_y - 8

            const_variacao_y = const_variacao_y - 8
        eixo_xx += 30
        const_variacao_y = altura_inicial


def plot_class(c, level, df, class_names_df, final_columns):
    eixo_x = 30

    altura_inicial = calculate_max_y(df, level)
    if level == 2:
        altura_inicial -= 5
    const_variacao_y = altura_inicial
    c.setFont("Helvetica-Bold", 5.4)
    c.drawString(eixo_x - 2.5, altura_inicial + 11, "ClassValue")
    c.drawString(eixo_x + 50, altura_inicial + 11, "ClassName")

    eixo_xx = eixo_x + 95
    for i in range(len(df)):
        if i < len(class_names_df):
            c.setFont("Helvetica-Bold", 5.4)
            if df['ClassValue'].iloc[i] == 'C_37':
                first_class = str(class_names_df['Classe'].iloc[i]).split(' e ')
                c.drawString(eixo_x + 38, const_variacao_y, first_class[0])
                c.drawString(eixo_x + 38, const_variacao_y - 7, f"e {first_class[1]}")
            else:
                c.drawString(eixo_x + 38, const_variacao_y, class_names_df['Classe'].iloc[i])

            c.setFont("Helvetica", 5)
            if len(class_names_df['Classe'].iloc[i]) <= 12:
                c.drawString(eixo_xx, altura_inicial + 10, class_names_df['Classe'].iloc[i])

            else:
                paragrafo_matriz_confusao(c, class_names_df['Classe'].iloc[i], eixo_xx, altura_inicial + 5, 30)

            eixo_xx += 30

            if i + 1 == len(class_names_df):
                c.drawString(eixo_xx + 7, altura_inicial + 10, final_columns[0])
                c.drawString(eixo_xx + 32, altura_inicial + 10, final_columns[1])
                c.drawString(eixo_xx + 66, altura_inicial + 10, final_columns[2])

        else:
            eixo_x = 64
            const_variacao_y = const_variacao_y - 1

        c.drawString(eixo_x, const_variacao_y, df['ClassValue'].iloc[i])

        if df['ClassValue'].iloc[i] == 'C_37':
            const_variacao_y = const_variacao_y - 8

        const_variacao_y = const_variacao_y - 8




def template_imagens_graficos(c, imagens_mapa_png, imagens_grafico_png):
    quantidade_imagens = len(imagens_mapa_png)

    imagens_excedidas = 0
    if quantidade_imagens > 5:
        imagens_excedidas = len(imagens_mapa_png) - 5

    quantidade_paginas = int(imagens_excedidas / 6) + 1

    background_padrao(c)

    if(quantidade_imagens > 6):
        if abs(len(imagens_grafico_png) - 5) != 0:
            quantidade_paginas += 1

        posicao = 0

        for i in range(quantidade_paginas):
            posicao_imagem_esq = [40, 298]
            posicao_imagem_dir = [245, 505]

            # Primeira Página, de algumas
            if i == 0:
                posicao_imagem_esq = [40, 190]
                posicao_imagem_dir = [245, 405]
                if quantidade_imagens < 5:
                    repeticao =  quantidade_imagens
                else:
                    repeticao =  5

                for j in range(repeticao):
                    c.drawImage(imagens_grafico_png[j], posicao_imagem_dir[0], posicao_imagem_dir[1], width=360, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_dir[1] -= 139

                    c.drawImage(imagens_mapa_png[j], posicao_imagem_esq[0], posicao_imagem_esq[1], width=220, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_esq[1] -= 139
                posicao += 5
                c.setFont("Helvetica", 10)
                paragrafos(c, "II - Pontos de referência e Índice de Vegetação Melhorado (EVI)", 56, 735, 1, 'justify')


            #Última
            elif i + 1 == quantidade_paginas:
                posicao_imagem_esq = [40, 298]
                posicao_imagem_dir = [245, 505]
                repeticoes = imagens_excedidas % 6

                for j in range(repeticoes):
                    c.drawImage(imagens_grafico_png[posicao + j], posicao_imagem_dir[0], posicao_imagem_dir[1], width=360, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_dir[1] -= 139

                    c.drawImage(imagens_mapa_png[posicao + j], posicao_imagem_esq[0], posicao_imagem_esq[1], width=220, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_esq[1] -= 139
                continue

            # Outras Páginas
            else:
                if quantidade_imagens < 6:
                    repeticao =  quantidade_imagens
                else:
                    repeticao =  6

                for j in range(repeticao):
                    c.drawImage(imagens_grafico_png[posicao + j], posicao_imagem_dir[0], posicao_imagem_dir[1], width=360, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_dir[1] -= 139

                    c.drawImage(imagens_mapa_png[posicao + j], posicao_imagem_esq[0], posicao_imagem_esq[1], width=220, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_esq[1] -= 139
                posicao += 6


            c.showPage()
            background_padrao(c)

    #Única Página
    else:
        posicao_imagem_esq = [40, 190]
        posicao_imagem_dir = [245, 405]
        for j in range(quantidade_imagens):
            c.drawImage(imagens_grafico_png[j], posicao_imagem_dir[0], posicao_imagem_dir[1], width=360, preserveAspectRatio=True, mask='auto')
            posicao_imagem_dir[1] -= 139

            c.drawImage(imagens_mapa_png[j], posicao_imagem_esq[0], posicao_imagem_esq[1], width=220, preserveAspectRatio=True, mask='auto')
            posicao_imagem_esq[1] -= 139

        c.setFont("Helvetica", 10)
        paragrafos(c, "II - Pontos de referência e Índice de Vegetação Melhorado (EVI)", 56, 735, 1, 'justify')


def template_imagens_graficos_1(c, imagens_mapa_png, imagens_grafico_png, altura):
    quantidade_imagens = len(imagens_mapa_png)

    imagens_excedidas = 0
    if quantidade_imagens > 2:
        imagens_excedidas = len(imagens_mapa_png) - 2

    quantidade_paginas = int(imagens_excedidas / 6) + 1

    background_padrao(c)

    if(quantidade_imagens > 2):
        if abs(len(imagens_grafico_png) - 2) != 0:
            quantidade_paginas += 1

        posicao = 0

        for i in range(quantidade_paginas):
            posicao_imagem_esq = [40, 298]
            posicao_imagem_dir = [245, 505]

            # Primeira Página, de algumas
            if i == 0:
                posicao_imagem_esq = [40, -1 * altura + 20]
                posicao_imagem_dir = [245, -30]

                for j in range(2):
                    c.drawImage(imagens_grafico_png[j], posicao_imagem_dir[0], posicao_imagem_dir[1], width=360, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_dir[1] -= 139

                    c.drawImage(imagens_mapa_png[j], posicao_imagem_esq[0], posicao_imagem_esq[1], width=220, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_esq[1] -= 139

                posicao = 2
                c.setFont("Helvetica", 10)
                paragrafos(c, "II - Pontos de referência e Índice de Vegetação Melhorado (EVI)", 56, altura + 45, 1, 'justify')


            #Última
            elif i + 1 == quantidade_paginas:
                posicao_imagem_esq = [40, 298]
                posicao_imagem_dir = [245, 505]
                repeticoes = imagens_excedidas % 6

                for j in range(repeticoes):
                    c.drawImage(imagens_grafico_png[posicao + j], posicao_imagem_dir[0], posicao_imagem_dir[1], width=360, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_dir[1] -= 139

                    c.drawImage(imagens_mapa_png[posicao + j], posicao_imagem_esq[0], posicao_imagem_esq[1], width=220, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_esq[1] -= 139
                continue

            # Outras Páginas
            else:
                if quantidade_imagens < 6:
                    repeticao =  quantidade_imagens
                else:
                    repeticao =  6

                for j in range(repeticao):
                    c.drawImage(imagens_grafico_png[posicao + j], posicao_imagem_dir[0], posicao_imagem_dir[1], width=360, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_dir[1] -= 139

                    c.drawImage(imagens_mapa_png[posicao + j], posicao_imagem_esq[0], posicao_imagem_esq[1], width=220, preserveAspectRatio=True, mask='auto')
                    posicao_imagem_esq[1] -= 139
                posicao += 6


            c.showPage()
            background_padrao(c)

    #Única Página
    else:
        posicao_imagem_esq = [40, -1 * altura + 20]
        posicao_imagem_dir = [245, -30]

        for j in range(2):
            c.drawImage(imagens_grafico_png[j], posicao_imagem_dir[0], posicao_imagem_dir[1], width=360, preserveAspectRatio=True, mask='auto')
            posicao_imagem_dir[1] -= 139

            c.drawImage(imagens_mapa_png[j], posicao_imagem_esq[0], posicao_imagem_esq[1], width=220, preserveAspectRatio=True, mask='auto')
            posicao_imagem_esq[1] -= 139

        c.setFont("Helvetica", 10)
        paragrafos(c, "II - Pontos de referência e Índice de Vegetação Melhorado (EVI)", 56, altura + 45, 1, 'justify')


def background_padrao(c):
    c.drawImage('./arquivos_relatorio/imagens/assets_pdf/barra_lateral.png', 0, -749, width=28.5, preserveAspectRatio=True, mask='auto')
    c.drawImage('./arquivos_relatorio/imagens/assets_pdf/Logo Vega.png', 45, 665, width=160, preserveAspectRatio=True, mask='auto')
    c.drawImage('./arquivos_relatorio/imagens/assets_pdf/site vega.png', 400, 785, width=165, preserveAspectRatio=True, mask='auto')
    