class NodeExplorer():
    """Cria objetos que representem os nós.
    """
    def __init__(self, i: int, items_taken: list, value: float, capacity: float, best_estimation: float):
        """Inicializador do nó.
        
        Args:
            i: índice do item a ser explorado no nó.
            items_taken: itens pegos até o momento, no formato 0 ou 1.
            value: valor agregado no nó (soma dos itens pegos).
            capacity: capacidade disponível para o nó (capacidade total menos o peso dos itens pegos).
            best_estimation: solução otimista para aquele nó.
        """
        self.i = i
        self.items_taken = items_taken
        self.value = value
        self.best_estimation = best_estimation
        self.capacity = capacity

class DepthFirstSearch():
    """Orquestrador da estratégia de busca.
    """
    
    def __init__(self, items: list, capacity: float):
        """Inicializador da busca.
        
        Args:
            items: conjunto de itens a ser explorado.
            capacity: capacidade máxima da mochila.
        """
        self.items = items
        self.capacity = capacity
        self.best = 0  # iniciamos nossa melhor solução com valor nulo
        self.items_taken = []  # e sem pegar nenhum item
        
        self.start_search()  # começa a busca
        self.collect_items()  # verifica quais itens foram pegos


    def sorting(self):
        """Ordena os itens por densidade de valor, da maior para a menor.
        """
        self.items = sorted(self.items, key=lambda x: x.weight/x.value)

    def best_possible_solution(self, items: list, k: float) -> float:
        """Retorna a solução otimista para um nó (usando relaxation de itens fracionários).
        
        Args:
            items: lista contendo o subconjunto de itens que serão analizados no nó (e seus nós filhos) em questão.
            k: capacidade disponível no nó.
            
        Returns:
            solução ótima para a configuração acima.
        """
        best_value = 0
        i = 0
        while k > 0 and i < len(items):  # enquanto ouver espaço na mochila, pegamos itens
            best_value += items[i].value
            k -= items[i].weight
            i += 1
        
        if k < 0:  # se o último item pego estourar a capacidade, pegamos apenas uma fração dele
            i -= 1
            best_value -= items[i].value
            k += items[i].weight
            best_value += k/items[i].weight*items[i].value
  
        return best_value

    def searchNode(self, node: object):
        """Faz a análise e exploração de um nó.
        
        Args:
            node: objeto que representa um nó.
        """
        if node.capacity < 0 or node.best_estimation < self.best:  # critérios de parada
            return None
        elif node.value > self.best:  # caso encontramos um valor maior que o melhor valor até o momento
            self.best = node.value
            self.items_taken = node.items_taken
        if node.i == len(self.items):  # no último item não exploramos seus filhos
            return None
        
        # nó a esquerda, no qual pegamos o item em questão
        node1 = NodeExplorer(
            node.i + 1,  # próximo item
            node.items_taken + [1],  # item pego
            node.value + self.items[node.i].value,  # adiciona o valor do item
            node.capacity - self.items[node.i].weight,  # remove da capacidade o peso do item
            node.best_estimation  # nossa melhor estimativa não muda, já que pegamos o item mais denso
        )
        
        # nó a direita, no qual não pegamos o item em questão
        node0 = NodeExplorer(
            node.i + 1,
            node.items_taken + [0],  # item não pego
            node.value,  # não adicionamos o valor do item
            node.capacity,  # capacidade disponível não muda, já que não pegamos o item
            node.value + self.best_possible_solution(self.items[node.i + 1:], node.capacity)  # não pegar o item mais denso nos  leva a atualizar a solução ótima, que será o valor do nó somado a solução ótima do filho
        )
        
        # depth-first: buscamos primeiramente sempre à esquerda
        self.searchNode(node1)
        self.searchNode(node0)
        
    def start_search(self):
        """Inicia a busca no primeiro nó.
        """
        self.sorting()  # ordenar para termos os itens mais valiosos no início (e podermos usar o relaxation)
        starterNode = NodeExplorer(
            0,  # começamos no primeiro item da lista
            [],  # não pegamos nenhum item
            0,  # nosso valor inicial é 0 (não pegamos nada ainda)
            self.capacity,  # começamos com a capacidade máxima da mochila
            self.best_possible_solution(self.items, self.capacity)  # solução otimista considera todos os items
        )
        self.searchNode(starterNode)

    def collect_items(self):
        """Verifica quais itens foram pegos.
        """
        items_taken = []
        for i in range(len(self.items_taken)):
            if self.items_taken[i] == 1:
                items_taken.append(self.items[i].index)
        self.items_taken = items_taken