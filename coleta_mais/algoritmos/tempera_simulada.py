import numpy as np 
import math
from back.comum import sucessoresMochila, sucessoresCv



def temperaSimulada(si, vi, problema, ti, tf, fr, tipo):
    solucao_atual = si
    melhorsolucao = si
    valor_atual = vi
    melhorvalor = vi
    temperatura = ti
    
    

    while temperatura > tf:

        if tipo == "mochila":
            solucao_nova,valor_novo = sucessoresMochila("tempera", solucao_atual, valor_atual, problema)
            diferenca = valor_novo - valor_atual
            if diferenca > 0:
                solucao_atual = solucao_nova
                valor_atual = valor_novo
                if valor_atual > melhorvalor:
                    melhorsolucao = solucao_atual
                    melhorvalor = valor_atual

            else:
                aleatorio = np.random.rand()
                diferenca *= -1 
                auxiliar = math.exp(-diferenca/temperatura)
                if aleatorio < auxiliar:
                    solucao_atual = solucao_nova
                    valor_atual = valor_novo
            temperatura *= fr





        else:
            solucao_nova,valor_novo = sucessoresCv("tempera", solucao_atual, valor_atual, problema)
            diferenca = valor_novo - valor_atual
            if diferenca < 0:
                solucao_atual = solucao_nova
                valor_atual = valor_novo
                if valor_atual < melhorvalor:
                    melhorsolucao = solucao_atual
                    melhorvalor = valor_atual
        
            else:
                aleatorio = np.random.rand()
        
                auxiliar = math.exp(-diferenca/temperatura)
                if aleatorio < auxiliar:
                    solucao_atual = solucao_nova
                    valor_atual = valor_novo
            temperatura *= fr


    return  melhorsolucao, melhorvalor
