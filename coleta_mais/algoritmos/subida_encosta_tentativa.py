from back.comum import sucessoresMochila, sucessoresCv

def subidaEncostaTentativa(si, vi, problema, tentativas, tipo):
    solucao_atual = si
    valor_atual = vi
    t = 0

    while t < tentativas:

        if tipo == "mochila":
            solucao_nova,valor_novo = sucessoresMochila("subida", solucao_atual, valor_atual, problema)

            
            if valor_novo > valor_atual:
                solucao_atual = solucao_nova
                valor_atual =valor_novo
                t = 0

            else:
                t += 1
        else:
            solucao_nova,valor_novo = sucessoresCv("subida", solucao_atual, valor_atual, problema)
            if valor_novo < valor_atual:       
                solucao_atual = solucao_nova
                valor_atual =valor_novo
                t = 0

            else:
                t += 1

    return solucao_atual, valor_atual
