import reflex as rx

from .estado import Estado
from .layout import area_resultados, area_vazia, botoes, campo, cartao, entrada, grade, pagina


def genetico():
    return pagina(
        "Algoritmos genéticos",
        "Configure a população e as taxas e execute o algoritmo sobre o problema gerado.",
        cartao(
            "Parâmetros genéticos",
            "Taxas entre 0 e 1 (por exemplo, 0,8 = 80%).",
            grade(
                campo("Tamanho da população", entrada("populacao", Estado.populacao)),
                campo("Número de gerações", entrada("geracoes", Estado.geracoes)),
                campo("Taxa de cruzamento", entrada("cruzamento", Estado.cruzamento)),
                campo("Taxa de mutação", entrada("mutacao", Estado.mutacao)),
                campo("Intervalo de geração", entrada("intervalo", Estado.intervalo)),
            ),
            botoes(Estado.executar_ag, Estado.analisar_ag),
        ),
        area_resultados(
            Estado.ag_res,
            Estado.ag_hist,
            area_vazia("dna", "Nenhuma execução ainda", "Ajuste os parâmetros e toque em Executar."),
        ),
    )
