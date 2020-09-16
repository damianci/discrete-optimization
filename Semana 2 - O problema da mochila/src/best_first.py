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

class MaxPQ():
    """Fila de prioridade de máximo. Utilizaremos um vetor para representar a fila.
        
        Nesse vetor, o índice i será pai dos índices 2*i e 2*i + 1. Um filho nunca poderá ser maior que seu pai.
    """
    def __init__(self):
        """Inicializador da fila.
        """
        self.pq = [0]  # para falicitar as operações, a posição inicial do vetor não será usuada
        self.length = 0
        
    def isEmpty(self):
        """Verifica se a fila está vazia.
        """
        return self.length == 0
    
    def swim(self, k: int):
        """Função suporte que atualiza a posição de um elemento na fila, quando ele possui pais menores que ele.
        
        Args:
            k: índice do elemento.
        """
        # como estamos falando de nós (definido no depth-first) devemos comparar o atributo best_estimation
        while k > 1 and self.pq[k//2].best_estimation < self.pq[k].best_estimation:  # enquanto o filho for maior que o pai
            self.pq[k//2], self.pq[k] = self.pq[k], self.pq[k//2]  # trocamos as posições
            k //= 2
    
    def insert(self, element: object):
        """Insere um novo nó na fila.
        
        Args:
            element: nó (objeto NodeExplorer).
        """
        self.length += 1
        self.pq.append(element)  # adicionamos sempre na última posição da lista
        self.swim(self.length)  # achamos a posição ideal para o nó adicionado
        
    def sink(self, k: int):
        """Função suporte que atualiza a posição de um elemento na fila, quando ele possui filhos maiores que ele.
        
        Args:
            k: índice do elemento.
        """
        while 2*k <= self.length:  # enquanto possuir filhos
            j = 2*k  # veja o filho da esquerda
            if j < self.length and self.pq[j].best_estimation < self.pq[j + 1].best_estimation:  # se possuir dois filhos
                j += 1  # aponte para o filho da direita caso ele seja maior
            if self.pq[k].best_estimation >= self.pq[j].best_estimation:  # se o pai for maior que o filho pare
                break
            self.pq[k], self.pq[j] = self.pq[j], self.pq[k]  # troque pai com filho
            k = j  # atualize o índice do elemento que estamos trabalhando
    
    def getMax(self) -> object:
        """Remove e retorna o objeto com o maior best_estimation.
        
        Returns:
            Nó com o maior best_estimation.
        """
        self.pq[1], self.pq[-1] = self.pq[-1], self.pq[1]  # troca o maior elemento pelo último
        obj = self.pq.pop()  # retira o último elemento (que agora é o maior)
        self.length -= 1
        self.sink(1)  # atualiza a posição do agora primeiro elemento
        
        return obj  # retorna o elemento

class BestFirstSearch():
    """Orquestrador da estratégia de busca.    
    """
    
    def __init__(self, items: list, capacity: float):
        """Inicializador.
        
        Args:
            items: conjunto de itens a ser explorado.
            capacity: capacidade máxima da mochila.
        """        
        self.items = items
        self.capacity = capacity
        self.best = 0  # iniciamos nossa melhor solução com valor nulo
        self.items_taken = []  # e sem pegar nenhum item
        self.priority_queue = MaxPQ()
        
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
        
        # adicionando os dois nós na fila de prioridade
        self.priority_queue.insert(node1)
        self.priority_queue.insert(node0)
        
        # enquanto a fila não estiver vazia e a melhor solução otimista for maior que a melhor solução
        while not(self.priority_queue.isEmpty()) and self.priority_queue.pq[1].best_estimation > self.best:
            self.searchNode(self.priority_queue.getMax())  # o próximo nó a ser explorado é o pop da fila     
        
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