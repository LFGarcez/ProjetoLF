import reflex as rx

from .estado import Estado
from .layout import area_resultados, area_vazia, botoes, campo, cartao, entrada, grade, pagina

# ----------------------------------------------------------------------
# Enquanto o algoritmo genético não existir (algoritmos/genetico.py com a
# função executar() e analisar_genetico() em back/analise.py), deixe True:
# a tela mostra só o aviso "Em desenvolvimento".
# Quando estiver pronto, mude para False e a tela completa volta.
# ----------------------------------------------------------------------
EM_DESENVOLVIMENTO = True

PARAMETROS_PREVISTOS = [
    "Tamanho da população",
    "Número de gerações",
    "Taxa de cruzamento",
    "Taxa de mutação",
    "Intervalo de geração",
]


def _em_desenvolvimento():
    return pagina(
        "Algoritmos genéticos",
        "Segunda etapa do projeto: resolver o mesmo problema de coleta com algoritmos genéticos.",
        rx.callout(
            "Em desenvolvimento. Os algoritmos genéticos ainda não estão disponíveis. "
            "Enquanto isso, a Busca local já resolve o problema.",
            icon="construction",
            color_scheme="amber",
            size="3",
            width="100%",
        ),
        cartao(
            "O que está previsto",
            "Quando o algoritmo estiver pronto, esta tela vai oferecer estes parâmetros:",
            rx.flex(
                *[rx.badge(nome, size="2", variant="soft") for nome in PARAMETROS_PREVISTOS],
                spacing="2",
                wrap="wrap",
            ),
            rx.text(
                "O resultado vai aparecer no mesmo formato da Busca local: lixo coletado, distância da rota, "
                "tempo, pontos escolhidos e ordem da rota.",
                color="var(--gray-11)",
                size="2",
            ),
            rx.link(
                rx.button(rx.icon("mountain", size=18), "Ir para a Busca local", size="3"),
                href="/busca-local",
                underline="none",
            ),
        ),
    )


def _tela_completa():
    """Tela do algoritmo genético já funcionando (usada quando EM_DESENVOLVIMENTO = False)."""
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


def genetico():
    return _em_desenvolvimento() if EM_DESENVOLVIMENTO else _tela_completa()