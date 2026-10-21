import reflex as rx

from .layout import icone_caminhao, pagina


def _etapa(numero, titulo, texto):
    return rx.card(
        rx.vstack(
            rx.center(rx.text(numero, weight="bold", color="var(--accent-contrast)"),
                      width="32px", height="32px", border_radius="50%", background="var(--accent-9)"),
            rx.heading(titulo, size="5"),
            rx.text(texto, color="var(--gray-11)"),
            align="start",
            spacing="2",
        ),
        size="3",
    )


def _info(rotulo, valor):
    return rx.flex(
        rx.text(rotulo, color="var(--gray-11)", min_width="130px"),
        rx.text(valor, weight="medium"),
        direction=rx.breakpoints(initial="column", sm="row"),
        padding_y="8px",
        border_bottom="1px solid var(--gray-5)",
        width="100%",
    )


def sobre():
    return pagina(
        "Coleta+",
        "Central de coleta de lixo que decide quais pontos o caminhão atende e em que ordem passa por eles.",
        icone_caminhao(),
        rx.grid(
            _etapa("1", "Problema da mochila",
                   "Cada ponto de coleta tem uma quantidade de resíduos. O algoritmo escolhe quantos pontos cabem na capacidade do caminhão."),
            _etapa("2", "Caixeiro viajante",
                   "Com os pontos escolhidos, o algoritmo define a ordem de passagem que gera o menor trajeto e economiza tempo."),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%",
        ),
        rx.card(
            rx.vstack(
                _info("Disciplina", "Programação Linear"),
                _info("Métodos", "Subida de encosta, subida com tentativas, têmpera simulada e algoritmos genéticos"),
                _info("Integrantes", "[Nome 1], [Nome 2], [Nome 3]"),
                _info("Professor(a)", "[Nome do professor]"),
                spacing="0",
                width="100%",
            ),
            size="3",
            width="100%",
        ),
    )
