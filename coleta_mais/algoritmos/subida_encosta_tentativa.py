
# ta para todos saberem como funciona: 
#a função é chama com os parametros: 
#si = solucao inicial, vi = valor inicial, p_max = parametro maximo, tentativas = numero de tentativas.

# a o valor de si e vi são transferidos para solucao_atual e valor_atual, respectivamente. 
# ( já que não passou o algoritimo eles são os atuais)


# e o t que é o contador de tentativas é inicializado com 0.
#( para registrar quantas vezes falharam em achar uma solução melhor e terminar quando acabar as tentativas)


#depois ele entra no while que verifica se não passou do numero de tentativas e chama a função sucessores e retorna o valores encontardos
#o o if verifica se a solução é melhor ( se o nove é menor por ser minimização o problema nosso)
#se não for ele vai pro else soma 1 em "t" para registrar tentativas e repete tudo

#carlos: qualquer coisa me perguntem 

def subida_encosta(si, vi, p_max, tentativas):
    solucao_atual = si
    valor_atual = vi
    t = 0

    while t < tentativas:
        sulucao_nova,valor_novo = sucessores(solucao_atual, valor_atual, p_max)

        
        if valor_novo > valor_atual:
            
            return solucao_atual, valor_atual

        solucao_atual = sulucao_nova
        valor_atual =valor_novo



    else:
        t += 1

