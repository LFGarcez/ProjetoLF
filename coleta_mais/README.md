# Coleta+

## Como rodar
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    reflex run

## Pastas
- `front/`      -> telas (não precisa mexer)
- `back/`       -> funcionalidades: gerar o problema e gerar os PDFs de análise  (SEU)
- `algoritmos/` -> subida de encosta, têmpera simulada e genético             (SEU)
- `assets/`     -> logos e cores (tema.css)

Cada arquivo de `back/` e `algoritmos/` tem no topo, em comentário, o nome
da função que a tela procura e o que ela deve devolver.
