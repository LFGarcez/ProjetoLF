import numpy as np 
CAPACIDADE_CAMINHAO = 20






 # n = qtd de pts. 

def gerarProblemaCV(pontos):

    # distan_min = menor valor de distancia. 
    distan_min = 1
    # distan_max = maior valor de distancia. 
    distan_max = 50

    # cria uma matriz n por n completa de 0
    matriz = np.zeros((pontos + 1, pontos + 1), dtype = int)

    # ai ele preenche com as distancias aleatorias menos a diagonal
    for i in range(pontos + 1):
        for j in range(i + 1, pontos + 1):

            # distancia aleatoria
            distancia = np.random.randint(distan_min, distan_max)
            # distancia de i ate j
            matriz[i][j] = distancia
            # distancia de j ate i SAO IGUAIS
            #para a matris ficar espelhada
            matriz[j][i] = distancia

    return matriz










 # n = qtd de pts.
def gerarProblemaMochila(pontos):

    # limite_min = menor qtd possivel de lixo. 
    limite_min = 1
    # limite_max = maior qtd posivel de lixo mas menor que a capacidade do caminhão.
    limite_max = CAPACIDADE_CAMINHAO

    # cria um vetor 
    lixo = np.random.randint(limite_min, limite_max, size = pontos + 1)# n+1 pq o deposito entra no vetor e a posicao 0 do vetor fica alinha com a da matriz 
    lixo[0] = 0 # o deposito nao tem lixo

    return lixo










 # une os dois gerarProblema
def gerarProblemaAleatorio(pontos):

    # gera a matriz do caixeiro viajante
    matriz = gerarProblemaCV(pontos)

    # gera o vetor de residuos
    lixo = gerarProblemaMochila(pontos )

    # junta todas as informacoes do problema
    problema = {
        "n": pontos,
        "distancias": matriz,
        "residuos": lixo,
        "capacidade": CAPACIDADE_CAMINHAO   
    }

    return problema 








def gerarProblemaFixo():


    problema = {
        "n": 5,
        "distancias": np.array([[0 , 19, 8 , 30, 8 , 19],
                                [19, 0 , 7 , 40, 13, 23],
                                [8 , 7 , 0 , 31, 14, 39],
                                [30, 40, 31, 0 , 12, 24],
                                [8 , 13, 14, 12, 0 , 40],
                                [19, 23, 39, 24, 40, 0 ]]),

        "residuos": np.array([0, 10, 8, 2, 11, 3]),
        "capacidade": CAPACIDADE_CAMINHAO   
    }

    return problema






    
def gerarProblema(tipo, pontos):

    if tipo == "aleatoria":
        resultado = gerarProblemaAleatorio(pontos)
    elif tipo == "fixa":
        resultado = gerarProblemaFixo()
    else:
        raise ValueError("Tipo de problema inválido. Escolha 'aleatoria' ou 'fixa'.")

    resultado["distancias"] = resultado["distancias"].tolist()
    resultado["residuos"] = resultado["residuos"].tolist()
   
    return resultado