def recursion_solution(k: int, j: int, items: list) -> float:
    """Função recursiva para encontrar a solução ótima para o problema da mochila.
    
    Args:
        k: tamanho da submochila
        j: itens considerados no subproblema (apenas os j primeiros)
        items: lista de namedtuple com todos os itens do problema
        
    Retorna:
        Solução ótima para a mochila de capacidade k, considerando apenas os j primeiros itens    
    """
    if j == -1:  # com j == -1 não estamos considerando nenhum item (começamos com index 0)
        return 0
    elif items[j].weight <= k:
        return max(
            recursion_solution(k, j - 1, items),
            items[j].value + recursion_solution(k - items[j].weight, j - 1, items)
        )
    else:
        return recursion_solution(k, j - 1, items)