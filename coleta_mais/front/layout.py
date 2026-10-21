"""Janela principal: menu lateral (computador), barra inferior (celular) e peças reutilizáveis."""
import reflex as rx

from .estado import Estado

MENU = [
    ("Sobre o trabalho", "Sobre", "/", "info"),
    ("Configurações", "Config.", "/configuracoes", "sliders-horizontal"),
    ("Busca local", "Busca", "/busca-local", "mountain"),
    ("Algoritmos genéticos", "AG", "/genetico", "dna"),
]


def logo(largura="150px"):
    return rx.color_mode_cond(
        light=rx.image(src="/logo_claro.png", width=largura, alt="Coleta+"),
        dark=rx.image(src="/logo_escuro.png", width=largura, alt="Coleta+"),
    )


def icone_caminhao(largura="260px"):
    return rx.color_mode_cond(
        light=rx.image(src="/icone_claro.png", width=largura, alt="Caminhão de coleta"),
        dark=rx.image(src="/icone_escuro.png", width=largura, alt="Caminhão de coleta"),
    )


def botao_tema():
    return rx.button(
        rx.color_mode_cond(light=rx.icon("moon", size=18), dark=rx.icon("sun", size=18)),
        rx.color_mode_cond(light="Tema escuro", dark="Tema claro"),
        on_click=rx.toggle_color_mode,
        variant="outline",
        size="3",
    )


def _item_lateral(nome, _curto, rota, icone):
    ativo = rx.State.router.page.path == rota
    return rx.link(
        rx.hstack(rx.icon(icone, size=20), rx.text(nome, weight="medium"), spacing="3", align="center"),
        href=rota,
        underline="none",
        width="100%",
        padding="12px 14px",
        border_radius="10px",
        background=rx.cond(ativo, "var(--accent-3)", "transparent"),
        color=rx.cond(ativo, "var(--accent-11)", "var(--gray-11)"),
    )


def _item_inferior(_nome, curto, rota, icone):
    ativo = rx.State.router.page.path == rota
    return rx.link(
        rx.vstack(rx.icon(icone, size=22), rx.text(curto, size="1", weight="medium"), spacing="1", align="center"),
        href=rota,
        underline="none",
        flex="1",
        padding="8px 2px",
        border_radius="10px",
        background=rx.cond(ativo, "var(--accent-3)", "transparent"),
        color=rx.cond(ativo, "var(--accent-11)", "var(--gray-11)"),
    )


def _barra_lateral():
    return rx.vstack(
        logo(),
        rx.vstack(*[_item_lateral(*m) for m in MENU], spacing="1", width="100%", margin_top="24px"),
        rx.spacer(),
        botao_tema(),
        position="sticky",
        top="0",
        height="100vh",
        width="260px",
        flex_shrink="0",
        padding="28px 20px",
        border_right="1px solid var(--gray-5)",
        align="start",
    )


def _barra_topo_celular():
    return rx.hstack(
        logo("96px"),
        rx.button(rx.color_mode_cond(light=rx.icon("moon", size=18), dark=rx.icon("sun", size=18)),
                  on_click=rx.toggle_color_mode, variant="outline", aria_label="Alternar tema"),
        justify="between",
        align="center",
        width="100%",
        padding="12px 18px",
        border_bottom="1px solid var(--gray-5)",
        position="sticky",
        top="0",
        z_index="10",
        background="var(--color-background)",
    )


def _barra_inferior():
    return rx.hstack(
        *[_item_inferior(*m) for m in MENU],
        position="fixed",
        bottom="0",
        left="0",
        right="0",
        z_index="20",
        padding="6px",
        background="var(--color-background)",
        border_top="1px solid var(--gray-5)",
        width="100%",
    )


def pagina(titulo, subtitulo, *conteudo):
    """Moldura de todas as telas. Para criar uma tela nova, use pagina('Título', 'Frase', ...)."""
    return rx.box(
        rx.mobile_and_tablet(_barra_topo_celular()),
        rx.hstack(
            rx.desktop_only(_barra_lateral()),
            rx.box(
                rx.heading(titulo, size="8", margin_bottom="8px"),
                rx.text(subtitulo, color="var(--gray-11)", size="4", margin_bottom="28px", max_width="60ch"),
                rx.vstack(*conteudo, spacing="5", width="100%"),
                flex="1",
                min_width="0",
                max_width="1040px",
                padding=["20px 18px 120px", "28px 28px 120px", "44px 56px 64px"],
            ),
            spacing="0",
            align="start",
            width="100%",
        ),
        rx.mobile_and_tablet(_barra_inferior()),
        width="100%",
        min_height="100vh",
    )


# ---------- Peças reutilizáveis ----------
def cartao(titulo, dica, *filhos):
    return rx.card(
        rx.vstack(
            rx.heading(titulo, size="5"),
            rx.text(dica, color="var(--gray-11)", size="2"),
            *filhos,
            spacing="3",
            align="start",
            width="100%",
        ),
        size="3",
        width="100%",
    )


def campo(rotulo, entrada, ativo=True):
    """Rótulo + campo. 'ativo' pode ser um valor fixo ou uma condição do Estado."""
    return rx.vstack(
        rx.text(rotulo, weight="medium", size="2"),
        entrada,
        spacing="1",
        align="start",
        width="100%",
        opacity=rx.cond(ativo, "1", "0.45"),
    )


def entrada(nome_campo, valor, ativo=True):
    return rx.input(
        type="number",
        value=valor,
        on_change=lambda v: Estado.definir(nome_campo, v),
        disabled=~ativo if not isinstance(ativo, bool) else (not ativo),
        size="3",
        width="100%",
    )


def grade(*filhos):
    return rx.grid(*filhos, columns=rx.breakpoints(initial="1", sm="2", md="3"), spacing="4", width="100%")


def botoes(on_executar, on_analise):
    return rx.flex(
        rx.button(rx.icon("play", size=18), "Executar", on_click=on_executar, size="3"),
        rx.button(rx.icon("file-text", size=18), "Análise (PDF)", on_click=on_analise, size="3", variant="outline"),
        spacing="3",
        wrap="wrap",
        width="100%",
    )


def area_vazia(icone, titulo, texto):
    return rx.center(
        rx.vstack(
            rx.icon(icone, size=34, color="var(--accent-9)"),
            rx.text(titulo, weight="bold"),
            rx.text(texto, color="var(--gray-11)", size="2", text_align="center"),
            align="center",
            spacing="1",
        ),
        min_height="170px",
        width="100%",
    )


def _linha(rotulo, valor):
    return rx.hstack(
        rx.text(rotulo, color="var(--gray-11)", min_width="150px"),
        rx.text(valor, weight="medium"),
        align="start",
        width="100%",
        padding_y="8px",
        border_bottom="1px solid var(--gray-5)",
    )


def area_resultados(resumo, historico, vazio):
    """Área de exibição das telas de busca local e AG."""
    return rx.card(
        rx.vstack(
            rx.heading("Resultados", size="4"),
            rx.cond(
                resumo.length() > 0,
                rx.vstack(
                    _linha("Melhor valor", resumo["valor"]),
                    _linha("Tempo", resumo["tempo"]),
                    _linha("Pontos escolhidos", resumo["selecionados"]),
                    _linha("Ordem da rota", resumo["rota"]),
                    rx.cond(
                        historico.length() > 0,
                        rx.vstack(
                            rx.text("Evolução do melhor valor", weight="medium", size="2", margin_top="12px"),
                            rx.recharts.line_chart(
                                rx.recharts.line(data_key="valor", stroke="var(--accent-9)", dot=False, type_="monotone"),
                                rx.recharts.x_axis(data_key="passo"),
                                rx.recharts.y_axis(),
                                rx.recharts.graphing_tooltip(),
                                data=historico,
                                width="100%",
                                height=260,
                            ),
                            width="100%",
                        ),
                    ),
                    width="100%",
                    spacing="0",
                ),
                vazio,
            ),
            width="100%",
            align="start",
        ),
        size="3",
        width="100%",
        min_height="240px",
    )
