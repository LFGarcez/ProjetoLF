"""Estado da aplicação: guarda o que aparece na tela e liga os botões ao back-end.

Aqui NÃO existe nenhum algoritmo. Cada botão lê os campos, valida e chama uma
função das pastas algoritmos/ e back/ (que são de vocês). Se a função ainda não existir, a tela
avisa com uma mensagem em vez de quebrar.
"""
import copy
from typing import Any

import reflex as rx

from . import ponte
from .ponte import NaoImplementado

# Arquivos do back-end que a tela chama direto (a Busca local passa pela ponte).
BK_PROBLEMA = "back.problema"
BK_ANALISE = "back.analise"
ALG_GENETICO = "algoritmos.genetico"


class CampoInvalido(Exception):
    """Algum campo da tela está vazio ou fora do intervalo."""


def _chamar(modulo, nome, *args):
    """Importa o arquivo `modulo` e chama a função `nome` dele."""
    return ponte.funcao(modulo, nome)(*args)


def _numero(texto, nome, minimo=None, maximo=None, inteiro=False):
    try:
        valor = float(str(texto).replace(",", "."))
    except ValueError:
        raise CampoInvalido(f"{nome}: digite um número.")
    if minimo is not None and valor < minimo:
        raise CampoInvalido(f"{nome}: o mínimo é {minimo}.")
    if maximo is not None and valor > maximo:
        raise CampoInvalido(f"{nome}: o máximo é {maximo}.")
    return int(valor) if inteiro else valor


def _lista(valor):
    """Aceita lista comum ou array do numpy e devolve lista comum."""
    return valor.tolist() if hasattr(valor, "tolist") else valor


def _resumir(resultado, rotulos, capacidade):
    """Transforma o dicionário do algoritmo em textos prontos para a tela."""
    def nome(i):
        return rotulos[i] if 0 <= i < len(rotulos) else f"Ponto {i}"

    def numero(chave, sufixo=""):
        try:
            return f"{float(resultado[chave]):g}{sufixo}"
        except (KeyError, TypeError, ValueError):
            return "—"

    def tempo():
        try:
            return f"{float(resultado['tempo']):.4f} s"
        except (KeyError, TypeError, ValueError):
            return "—"

    rota = [int(i) for i in _lista(resultado.get("rota", []))]
    selecionados = [int(i) for i in _lista(resultado.get("selecionados", []))]
    if not rota:
        texto_rota = "—"
    elif resultado.get("buscou_rota", True):
        texto_rota = " → ".join([nome(0)] + [nome(i) for i in rota] + [nome(0)])
    else:
        texto_rota = " → ".join([nome(0)] + [nome(i) for i in rota] + [nome(0)]) + "  (poucos pontos: a ordem não muda a distância)"
    textos = {
        "lixo": numero("lixo", f" de {capacidade}"),
        "distancia": numero("distancia"),
        "tempo": tempo(),
        "selecionados": ", ".join(nome(i) for i in selecionados) or "—",
        "rota": texto_rota,
    }
    historico = [
        {"passo": i + 1, "valor": float(v)}
        for i, v in enumerate(_lista(resultado.get("historico", [])))
    ]
    return textos, historico


def _baixar(caminho):
    with open(caminho, "rb") as arquivo:
        dados = arquivo.read()
    return rx.download(data=dados, filename=str(caminho).replace("\\", "/").split("/")[-1])


class Estado(rx.State):
    # ---------- Configurações ----------
    tipo: str = "fixa"
    tamanho: str = "10"
    n: int = 0
    capacidade: int = 0
    residuos: list[int] = []
    distancias: list[list[int]] = []
    rotulos: list[str] = []

    # ---------- Busca local ----------
    metodo: str = "subida"
    tentativas: str = "10"
    temp_inicial: str = "1000"
    temp_final: str = "1"
    fator: str = "0.95"
    busca_res: dict[str, str] = {}
    busca_hist: list[dict[str, Any]] = []

    # ---------- Algoritmos genéticos ----------
    populacao: str = "50"
    geracoes: str = "100"
    cruzamento: str = "0.8"
    mutacao: str = "0.05"
    intervalo: str = "10"
    ag_res: dict[str, str] = {}
    ag_hist: list[dict[str, Any]] = []

    # ---------- Utilidades ----------
    def definir(self, campo: str, valor: str):
        """Guarda o que foi digitado em qualquer campo da tela."""
        setattr(self, campo, valor)

    @rx.var
    def tem_problema(self) -> bool:
        return len(self.residuos) > 0

    @rx.var
    def residuo_total(self) -> int:
        return sum(self.residuos)

    @rx.var
    def tabela_lixo(self) -> list[dict[str, Any]]:
        """Linhas da tabela de resíduos: um item por ponto de coleta (sem o depósito)."""
        return [{"rotulo": self.rotulos[i], "residuo": self.residuos[i]}
                for i in range(1, len(self.residuos))]

    @rx.var
    def tabela_distancias(self) -> list[list[str]]:
        """Linhas da matriz: o primeiro item de cada linha é o nome do ponto."""
        return [[self.rotulos[i]] + [str(d) for d in linha] for i, linha in enumerate(self.distancias)]

    def _problema(self):
        return {
            "pontos": self.n,
            "n": self.n,
            "distancias": copy.deepcopy(self.distancias),
            "residuos": copy.deepcopy(self.residuos),
            "capacidade": self.capacidade,
        }

    def _exige_problema(self):
        if not self.residuos:
            raise CampoInvalido("Gere um problema na tela Configurações primeiro.")

    # ---------- Botões ----------
    def gerar(self):
        try:
            tamanho = None
            if self.tipo == "aleatoria":
                tamanho = _numero(self.tamanho, "Tamanho do problema", 2, inteiro=True)
            problema = _chamar(BK_PROBLEMA, "gerarProblema", self.tipo, tamanho)
            residuos = [int(v) for v in _lista(problema["residuos"])]
            distancias = [[int(v) for v in linha] for linha in _lista(problema["distancias"])]
            if len(distancias) != len(residuos) or any(len(l) != len(residuos) for l in distancias):
                raise CampoInvalido("O problema está inconsistente: 'distancias' e 'residuos' precisam ter o mesmo tamanho.")
            self.residuos = residuos
            self.distancias = distancias
            self.capacidade = int(problema["capacidade"])
            self.n = len(residuos) - 1
            self.rotulos = ["Depósito"] + [f"Ponto {i}" for i in range(1, len(residuos))]
            self.busca_res, self.busca_hist = {}, []
            self.ag_res, self.ag_hist = {}, []
        except (NaoImplementado, CampoInvalido) as erro:
            return rx.toast.warning(str(erro))
        except Exception as erro:
            return rx.toast.error(f"Erro no back-end: {erro}")

    def executar_busca(self):
        try:
            self._exige_problema()
            parametros = {}
            if self.metodo == "tentativas":
                parametros["tentativas"] = _numero(self.tentativas, "Total de tentativas", 1, inteiro=True)
            if self.metodo == "tempera":
                parametros["temp_inicial"] = _numero(self.temp_inicial, "Temperatura inicial", 0)
                parametros["temp_final"] = _numero(self.temp_final, "Temperatura final", 0)
                parametros["fator"] = _numero(self.fator, "Fator redutor", 0.001, 0.999)
                if parametros["temp_final"] >= parametros["temp_inicial"]:
                    raise CampoInvalido("A temperatura final deve ser menor que a inicial.")
            problema = self._problema()
            if self.metodo == "subida":
                resultado = ponte.executar_subida(problema)
            elif self.metodo == "tentativas":
                resultado = ponte.executar_tentativas(problema, parametros["tentativas"])
            else:
                resultado = ponte.executar_tempera(problema, parametros["temp_inicial"],
                                                   parametros["temp_final"], parametros["fator"])
            self.busca_res, self.busca_hist = _resumir(resultado, self.rotulos, self.capacidade)
        except (NaoImplementado, CampoInvalido) as erro:
            return rx.toast.warning(str(erro))
        except Exception as erro:
            return rx.toast.error(f"Erro no back-end: {erro}")

    def analisar_busca(self):
        try:
            self._exige_problema()
            return _baixar(_chamar(BK_ANALISE, "analisar_busca_local", self._problema()))
        except (NaoImplementado, CampoInvalido) as erro:
            return rx.toast.warning(str(erro))
        except Exception as erro:
            return rx.toast.error(f"Erro no back-end: {erro}")

    def executar_ag(self):
        try:
            self._exige_problema()
            populacao = _numero(self.populacao, "Tamanho da população", 2, inteiro=True)
            geracoes = _numero(self.geracoes, "Número de gerações", 1, inteiro=True)
            cruzamento = _numero(self.cruzamento, "Taxa de cruzamento", 0, 1)
            mutacao = _numero(self.mutacao, "Taxa de mutação", 0, 1)
            intervalo = _numero(self.intervalo, "Intervalo de geração", 1, inteiro=True)
            resultado = _chamar(ALG_GENETICO, "executar", self._problema(),
                                populacao, geracoes, cruzamento, mutacao, intervalo)
            self.ag_res, self.ag_hist = _resumir(resultado, self.rotulos, self.capacidade)
        except (NaoImplementado, CampoInvalido) as erro:
            return rx.toast.warning(str(erro))
        except Exception as erro:
            return rx.toast.error(f"Erro no back-end: {erro}")

    def analisar_ag(self):
        try:
            self._exige_problema()
            return _baixar(_chamar(BK_ANALISE, "analisar_genetico", self._problema()))
        except (NaoImplementado, CampoInvalido) as erro:
            return rx.toast.warning(str(erro))
        except Exception as erro:
            return rx.toast.error(f"Erro no back-end: {erro}")