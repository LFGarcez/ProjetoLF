from back.comum import sucessoresMochila, sucessoresCv

def subida_encosta(si, vi, problema, tipo):
    solucao_atual = si
    valor_atual = vi


    while True:
    
            if tipo == "mochila":
                solucao_nova,valor_novo = sucessoresMochila("subida", solucao_atual, valor_atual, problema)
    
                
                if valor_novo > valor_atual:
                    solucao_atual = solucao_nova
                    valor_atual =valor_novo
                    
    
                else:
                    return solucao_atual, valor_atual
            else:
                solucao_nova,valor_novo = sucessoresCv("subida", solucao_atual, valor_atual, problema)
                if valor_novo < valor_atual:       
                    solucao_atual = solucao_nova
                    valor_atual =valor_novo
                    
    
                else:
                    return solucao_atual, valor_atual
    
        
        
