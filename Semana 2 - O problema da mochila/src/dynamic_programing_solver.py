def dynamic_programing_solver(items: list, capacity: int) -> tuple:
    """Resolve o problema da mochila através de programação dinâmica.
    
    Args:
        items: lista de namedtuple contendo todos os itens
        capacity: capacidade máxima da mochila
    
    Returns:
        S: tabela com todas as subsoluções
        taken: itens presentes na solução ótima
    """
    n_items = len(items)
    S = []
    for i in range(len(items) + 1):  # iniciando a tabela com zeros
        S += [[0]*(capacity + 1)]
        
    for i in range(n_items):  #  para cada item
        for k in range(capacity + 1):  # para todas as capacidades
            if items[i].weight <= k:  # se o item couber, podemos pegá-lo ou não
                S[i + 1][k] = max(
                    S[i + 1 - 1][k],
                    S[i + 1 - 1][k - items[i].weight] + items[i].value
                )  # lógica descrita acima. O item i é considerado na linha i + 1 (primeira linha considera nenhum item)
            else:  # se não couber, a solução é a mesma da que não considera esse item
                S[i + 1][k] = S[i + 1 - 1][k]
    
    # items presentes na solução ótima
    k = capacity
    taken = []
    for i in range(n_items - 1, -1, -1):  # começamos no último item/coluna
        if S[i + 1][k] != S[i + 1 - 1][k]:  # se o valor ótimo for diferente do imediatamente acima, o item foi pego
            taken.append(items[i].index)
            k = k - items[i].weight  # descontamos o peso do item
    
    return S, taken