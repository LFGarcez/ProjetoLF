"""Ponte entre a tela e as funções do back-end de vocês.

Aqui NÃO existe nenhum algoritmo, nenhuma avaliação e nenhum sorteio. Este
arquivo só CHAMA, na ordem certa, as funções que vocês já escreveram:

    1) back.comum.solucaoInicialMochila / solucaoInicialCv -> solução inicial
       (as duas já devolvem também o valor da solução)
    2) algoritmos.*                                        -> a busca em si

e monta o dicionário que a tela mostra. Se alguma função ainda não existir,
a tela mostra um aviso dizendo qual falta (nada quebra).

Fluxo de cada botão "Executar" da Busca local:
    mochila  ->  escolhe os pontos que cabem no caminhão
    caixeiro ->  ordena os pontos escolhidos (só se forem 3 ou mais)
"""
import importlib
import time


class NaoImplementado(Exception):
    """A função (ou o arquivo) do back-end ainda não foi criada."""


# ---- nomes que a ponte procura no back-end (mudem aqui se mudarem lá) ----
COMUM = "back.comum"
F_INICIAL_MOCHILA = "solucaoInicialMochila"  # (problema)         -> (mochila, lixo coletado)
F_INICIAL_CV = "solucaoInicialCv"            # (mochila, problema) -> (rota, distância total)

ARQ_SUBIDA, F_SUBIDA = "algoritmos.subida_encosta", "subida_encosta"
ARQ_TENTATIVAS, F_TENTATIVAS = "algoritmos.subida_encosta_tentativa", "subidaEncostaTentativa"
ARQ_TEMPERA, F_TEMPERA = "algoritmos.tempera_simulada", "temperaSimulada"

# Com menos pontos que isso não existe rota para melhorar (a rota só muda
# de ordem e a distância é a mesma), então a busca do caixeiro é pulada.
MIN_PONTOS_CAIXEIRO = 3


def funcao(modulo, nome):
    """Importa o arquivo `modulo` e devolve a função `nome`, ou avisa que falta."""
    arquivo = modulo.replace(".", "/") + ".py"
    try:
        mod = importlib.import_module(modulo)
    except ModuleNotFoundError as erro:
        if erro.name in (modulo, modulo.split(".")[0]):
            raise NaoImplementado(f"Falta criar o arquivo {arquivo}")
        raise
    achada = getattr(mod, nome, None)
    if achada is None:
        raise NaoImplementado(f"Falta criar {nome}() em {arquivo}")
    return achada


def _executar(problema, rodar_busca):
    """Roda as duas etapas e devolve o dicionário de resultado.

    rodar_busca(solucao, valor, problema, tipo) -> (solucao, valor)
        é a chamada do algoritmo escolhido; `tipo` é "mochila" ou "caixeiro".
    """
    inicial_mochila = funcao(COMUM, F_INICIAL_MOCHILA)
    inicial_cv = funcao(COMUM, F_INICIAL_CV)

    inicio = time.perf_counter()

    # ---- etapa 1: mochila (quais pontos o caminhão leva) ----
    mochila, lixo = inicial_mochila(problema)
    mochila, lixo = rodar_busca(mochila, lixo, problema, "mochila")

    # ---- etapa 2: caixeiro (em que ordem passa pelos pontos escolhidos) ----
    # A rota é refeita a partir da mochila FINAL, porque a busca pode ter
    # trocado os pontos escolhidos.
    rota, distancia = inicial_cv(mochila, problema)
    if len(rota) - 1 >= MIN_PONTOS_CAIXEIRO:
        rota, distancia = rodar_busca(rota, distancia, problema, "caixeiro")

    return {
        "lixo": lixo,
        "distancia": distancia,
        "tempo": time.perf_counter() - inicio,
        "selecionados": [i for i in range(1, len(mochila)) if mochila[i] == 1],
        "rota": list(rota[1:]),  # sem o depósito: a tela o coloca no começo e no fim
        "buscou_rota": len(rota) - 1 >= MIN_PONTOS_CAIXEIRO,
    }


def executar_subida(problema):
    subida = funcao(ARQ_SUBIDA, F_SUBIDA)
    return _executar(problema, lambda s, v, p, tipo: subida(s, v, p, tipo))


def executar_tentativas(problema, tentativas):
    subida = funcao(ARQ_TENTATIVAS, F_TENTATIVAS)
    return _executar(problema, lambda s, v, p, tipo: subida(s, v, p, tentativas, tipo))


def executar_tempera(problema, temp_inicial, temp_final, fator):
    tempera = funcao(ARQ_TEMPERA, F_TEMPERA)
    return _executar(problema, lambda s, v, p, tipo: tempera(s, v, p, temp_inicial, temp_final, fator, tipo))
