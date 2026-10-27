import reflex as rx

from .layout import cartao, icone_caminhao, pagina


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
        rx.text(rotulo, color="var(--gray-11)", min_width="170px", flex_shrink="0"),
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
        cartao(
            "O problema",
            "Coleta de lixo com um caminhão de capacidade limitada.",
            rx.text(
                "Uma central tem um depósito e vários pontos de coleta, cada um com uma quantidade de resíduos. "
                "O caminhão tem capacidade limitada e não consegue atender todos os pontos. "
                "Por isso o problema é resolvido em duas etapas: primeiro se escolhe quais pontos o caminhão atende "
                "e depois a ordem em que ele passa por eles.",
            ),
        ),
        rx.grid(
            _etapa("1", "Problema da mochila",
                   "Decide quais pontos o caminhão atende: o objetivo é maximizar o lixo coletado "
                   "sem passar da capacidade do caminhão."),
            _etapa("2", "Caixeiro viajante",
                   "Com os pontos escolhidos, decide em que ordem passar por eles: o objetivo é a menor "
                   "distância, saindo e voltando ao depósito."),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="4",
            width="100%",
        ),
        rx.card(
            rx.vstack(
                _info("Disciplina", "Programação Linear"),
                _info("Integrantes", "Carlos Henrique, Luis Felipe, Reginaldo Lopes e Sarah Nunes"),
                _info("Professor", "Luis Fernando"),
                spacing="0",
                width="100%",
            ),
            size="3",
            width="100%",
        ),
    )