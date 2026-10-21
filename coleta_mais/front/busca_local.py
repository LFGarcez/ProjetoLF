import reflex as rx

from .estado import Estado
from .layout import area_resultados, area_vazia, botoes, campo, cartao, entrada, grade, pagina


def _opcao(valor, texto):
    return rx.text(
        rx.hstack(rx.radio_group.item(value=valor), texto, spacing="2", align="center"),
        as_="label",
        size="3",
    )


def busca_local():
    tentativas = Estado.metodo == "tentativas"
    tempera = Estado.metodo == "tempera"
    return pagina(
        "Busca local",
        "Escolha um método, ajuste os parâmetros e execute sobre o problema gerado.",
        cartao(
            "Método",
            "Os campos de cada método são liberados conforme a escolha.",
            rx.radio_group.root(
                rx.vstack(
                    _opcao("subida", "Subida de encosta"),
                    _opcao("tentativas", "Subida de encosta com tentativas"),
                    _opcao("tempera", "Têmpera simulada"),
                    spacing="3",
                ),
                value=Estado.metodo,
                on_change=lambda v: Estado.definir("metodo", v),
            ),
            grade(
                campo("Total de tentativas", entrada("tentativas", Estado.tentativas, tentativas), tentativas),
                campo("Temperatura inicial", entrada("temp_inicial", Estado.temp_inicial, tempera), tempera),
                campo("Temperatura final", entrada("temp_final", Estado.temp_final, tempera), tempera),
                campo("Fator redutor", entrada("fator", Estado.fator, tempera), tempera),
            ),
            botoes(Estado.executar_busca, Estado.analisar_busca),
        ),
        area_resultados(
            Estado.busca_res,
            Estado.busca_hist,
            area_vazia("mountain", "Nenhuma execução ainda", "Escolha um método e toque em Executar."),
        ),
    )
