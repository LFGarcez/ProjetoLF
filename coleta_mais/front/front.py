"""Ponto de entrada do front: cria o app e registra as telas. Rodar com:  reflex run"""
import reflex as rx

from .busca_local import busca_local
from .configuracoes import configuracoes
from .genetico import genetico
from .sobre import sobre

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600&display=swap",
        "/tema.css",
    ],
)
app.add_page(sobre, route="/", title="Coleta+ | Sobre")
app.add_page(configuracoes, route="/configuracoes", title="Coleta+ | Configurações")
app.add_page(busca_local, route="/busca-local", title="Coleta+ | Busca local")
app.add_page(genetico, route="/genetico", title="Coleta+ | Algoritmos genéticos")
