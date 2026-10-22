import numpy as np 





# não sei se precisa tratar caso apessoa peça só um ponto
def sucessoresCv(algoritmo, solucao_atual, valor_atual, problema):
    posicao = np.random.randint(1, len(solucao_atual))
    sucessores = []
    valor_novo = 0

    for i in range(1, len(solucao_atual)):
        solucao_nova = solucao_atual.copy()
        valor_novo = 0
        if i == posicao:

            continue


        aux = solucao_nova[posicao]
        solucao_nova[posicao] = solucao_nova[i]
        solucao_nova[i] = aux  


        for j in range(0, len(solucao_atual) - 1 ):
                if j == len(solucao_atual) - 2:
                    valor_novo += problema["distancias"][solucao_nova[j + 1]][solucao_nova[0]]
                                   
                valor_novo += problema["distancias"][solucao_nova[j]][solucao_nova[j + 1]]

        sucessores.append([solucao_nova, valor_novo])



    #if subida return maior valor 
    if algoritmo == "subida":

        for i in range(0, len(sucessores)):
            if sucessores[i][1] < sucessores[0][1]:
                sucessores[0] = sucessores[i]

        return sucessores[0]    

    #if tempera return array de solucao aleatoria
    if algoritmo == "tempera":
        return sucessores[np.random.randint(0, len(sucessores))]


    













"""
Gera os vizinhos de uma solução da mochila e devolve UM deles.

solucao_atual -> lista de 0 e 1. A posição i vale 1 se o caminhão
                 coleta o ponto i. A posição 0 é o depósito e nunca muda.
valor_atual   -> quanto de lixo a solução atual coleta (soma do lixo dos 1).
problema      -> dicionário com "pontos" (quantidade de pontos de coleta),
                 "residuos" (lixo de cada ponto) e "capacidade".
algoritimo    -> "subida" devolve o MELHOR vizinho,
                 "tempera" devolve um vizinho SORTEADO.

Devolve [solucao_nova, valor_novo].
Regras: a solução original nunca é alterada e nenhum vizinho
passa da capacidade do caminhão.
"""
def sucessoresMochila(algoritmo, solucao_atual, valor_atual, problema):
    # Lista onde guardamos cada vizinho encontrado, no formato [solucao, valor].
    sucessores = []


    # Conta quantos vizinhos de ADIÇÃO foram achados.
    # Enquanto for 0, o while continua tentando.
    alteracao = 0


    # Cópia de trabalho. A REMOÇÃO altera esta cópia, nunca a original.
    # Os vizinhos de adição são feitos a partir dela.
    solucao_base = solucao_atual.copy()


    valor_base = valor_atual


    # Guarda o último ponto removido, para ele não ser recolocado logo em seguida
    # (se voltasse, o vizinho seria igual à solução original).
    # -1 significa "nenhum ponto removido ainda".
    pula = -1


    # Repete até existir pelo menos um vizinho.
    # Assim a lista nunca fica vazia e não dá erro na escolha lá embaixo.
    while alteracao == 0:


     # ETAPA 1: tentar ADICIONAR um ponto, um de cada vez.
     # O laço começa em 1 para pular o depósito (posição 0).
     for i in range(1, problema["pontos"] + 1):
        
        # Não recolocar o ponto que acabou de ser removido.
        if pula == i:
                    continue

        solucao_nova = solucao_base.copy()
        valor_novo = valor_base


        # Só dá para adicionar um ponto que ainda não está no caminhão.
        if solucao_nova[i] == 0:

            if valor_novo + problema["residuos"][i] <= problema["capacidade"]:


                solucao_nova[i] = 1
                valor_novo += problema["residuos"][i]

                alteracao += 1
                sucessores.append([solucao_nova, valor_novo])            
                


     # ETAPA 2: nenhuma adição coube (caminhão cheio).
     # Então REMOVE um ponto da base e o while tenta adicionar de novo.
     # O vizinho final acaba sendo uma TROCA: sai um ponto e entra outro.
     if alteracao == 0:
        for i in range(1, problema["pontos"] + 1):

             # Acha o primeiro ponto marcado e tira da BASE.
             if solucao_nova[i] == 1:
     
                 solucao_base[i] = 0
                 pula = i # lembra qual ponto saiu
                 valor_base -= problema["residuos"][i] # o caminhão ficou mais leve        
                 break


                
#if subida return maior valor 
    if algoritmo == "subida":

        for i in range(0, len(sucessores)):
            if sucessores[i][1] > sucessores[0][1]:
                sucessores[0] = sucessores[i]

        return sucessores[0]    

#if tempera return array de solucao aleatoria
    if algoritmo == "tempera":
        return sucessores[np.random.randint(0, len(sucessores))]



