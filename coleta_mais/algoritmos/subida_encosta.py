
# ta para todos saberem como funciona: 
#a função é chama com os parametros: 
#si = solucao inicial, vi = valor inicial, p_max = parametro maximo.


# a o valor de si e vi são transferidos para solucao_atual e valor_atual, respectivamente. 
# ( já que não passou o algoritimo eles são os atuais)


#depois ele entra no while
#o o if verifica se a solução é melhor ( se o nove é menor por ser minimização o problema nosso)
#se não for ele vai pro else e retorna a soluação atual e o valor atual


#carlos: qualquer coisa me perguntem 


def subida_encosta(si, vi, p_max):
    solucao_atual = si
    valor_atual = vi


    while True:
        sulucao_nova,valor_novo = sucessores(solucao_atual, valor_atual, p_max)
        
        if valor_novo <= valor_atual:

            return solucao_atual, valor_atual

        
        solucao_atual = sulucao_nova
        valor_atual =valor_novo


    else:
        return solucao_atual, valor_atual