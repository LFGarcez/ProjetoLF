import reflex as rx

from .estado import Estado
from .layout import area_vazia, campo, cartao, entrada, grade, pagina


def _tabela_lixo():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Ponto"),
                rx.table.column_header_cell("Resíduos"),
            )
        ),
        rx.table.body(
            rx.foreach(
                Estado.tabela_lixo,
                lambda p: rx.table.row(
                    rx.table.cell(p["rotulo"]),
                    rx.table.cell(p["residuo"]),
                ),
            )
        ),
        width="100%",
    )


def _tabela_distancias():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell(""),
                rx.foreach(Estado.rotulos, lambda r: rx.table.column_header_cell(r)),
            )
        ),
        rx.table.body(
            rx.foreach(
                Estado.tabela_distancias,
                lambda linha: rx.table.row(
                    rx.foreach(linha, lambda c, i: rx.table.cell(c, font_weight=rx.cond(i == 0, "700", "400"))),
                ),
            )
        ),
        width="100%",
    )


def configuracoes():
    aleatoria = Estado.tipo == "aleatoria"
    return pagina(
        "Configurações",
        "Defina o problema que os métodos vão resolver: depósito, pontos de coleta, resíduos de cada ponto e capacidade do caminhão.",
        cartao(
            "Problema",
            "Fixa usa sempre os mesmos dados. Aleatória cria um problema novo com o tamanho escolhido.",
            grade(
                campo(
                    "Tipo de execução",
                    rx.segmented_control.root(
                        rx.segmented_control.item("Fixa", value="fixa"),
                        rx.segmented_control.item("Aleatória", value="aleatoria"),
                        value=Estado.tipo,
                        on_change=lambda v: Estado.definir("tipo", v),
                        size="3",
                        width="100%",
                    ),
                ),
                campo("Tamanho do problema (pontos de coleta)", entrada("tamanho", Estado.tamanho, aleatoria), aleatoria),
            ),
            rx.button(rx.icon("refresh-cw", size=18), "Gerar problema", on_click=Estado.gerar, size="3"),
        ),
        rx.card(
            rx.vstack(
                rx.heading("Problema gerado", size="4"),
                rx.cond(
                    Estado.tem_problema,
                    rx.vstack(
                        rx.hstack(
                            rx.badge("Capacidade: " + Estado.capacidade.to_string(), size="2"),
                            rx.badge("Pontos de coleta: " + Estado.n.to_string(), size="2"),
                            rx.badge("Resíduo total: " + Estado.residuo_total.to_string(), size="2"),
                            wrap="wrap",
                        ),
                        rx.text("Resíduos por ponto (o depósito não tem resíduos)", weight="medium", size="2"),
                        rx.box(_tabela_lixo(), overflow_x="auto", width="100%"),
                        rx.text("Distâncias entre os pontos (linha = origem, coluna = destino)", weight="medium", size="2", margin_top="8px"),
                        rx.box(_tabela_distancias(), overflow_x="auto", width="100%"),
                        width="100%",
                        spacing="3",
                    ),
                    area_vazia("map-pin", "Nenhum problema gerado",
                               "Toque em Gerar problema para ver os pontos de coleta e a quantidade de resíduos de cada um."),
                ),
                width="100%",
                align="start",
            ),
            size="3",
            width="100%",
            min_height="240px",
        ),
    )
