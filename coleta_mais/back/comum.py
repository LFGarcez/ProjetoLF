import numpy as np 

def sucessores(solucao_atual, valor_atual, p_max):
    posicao = np.random.randint(0, p_max)


    for i in range(0, p_max):
        solucao_nova = solucao_atual.copy()

        if i == posicao:
            continue

        aux = solucao_nova[posicao]
        solucao_nova[posicao] = solucao_nova[i]
        solucao_nova[i] = aux



#for i in range(0, p_max):
#   if(i+1 == p_max): 
#       soma += matriz[solucao_nova[i], solucao_nova[0]] 
#       break
#
#   soma += matriz[solucao_nova[i], solucao_nova[i+1]]
#       
    valor_novo = np.sum(solucao_nova)
    

