
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from front import ponte


def analisar_busca_local(problema):
    # Executa os três algoritmos
    resultados = [
        ("Subida de Encosta", ponte.executar_subida(problema)),
        ("Subida com Tentativas", ponte.executar_tentativas(problema, 10)),
        ("Têmpera Simulada", ponte.executar_tempera(problema, 1000, 1, 0.95)),
    ]

    # Cria o PDF
    arquivo = "relatorio_busca_local.pdf"
    pdf = SimpleDocTemplate(arquivo)
    estilos = getSampleStyleSheet()
    conteudo = []

    conteudo.append(
        Paragraph("Analise Comparativa - Busca Local", estilos["Title"])
    )
    conteudo.append(Spacer(1, 20))

    # Monta a tabela de resultados
    dados = [
        ["Algoritmo", "Lixo coletado", "Distancia", "Tempo (s)"]
    ]

    for nome, resultado in resultados:
        dados.append([
            nome,
            str(resultado["lixo"]),
            str(resultado["distancia"]),
            f'{resultado["tempo"]:.4f}'
        ])

    tabela = Table(dados)
    tabela.setStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 8),
    ])

    conteudo.append(tabela)
    conteudo.append(Spacer(1, 20))
    conteudo.append(
        Paragraph(
            "O tempo representa a duracao da execucao de cada algoritmo. "
            "A quantidade de lixo deve ser maximizada e a distancia da rota "
            "deve ser minimizada.",
            estilos["Normal"]
        )
    )

    pdf.build(conteudo)

    # Devolve o caminho para o botão baixar o arquivo
    return arquivo
