from collections import namedtuple

def read_items(file_location: str) -> tuple:
    """Função usada para ler os arquivos que contém informações sobre a mochila.

    Args:
        file_location: string no formato "data/nome_arquivo"

    Returns:
        tupla contendo a capacidade da mochila, o número de itens e uma lista de namedtuple contendo os itens    
    """
    Item = namedtuple('Item', ['index', 'value', 'weight'])  # vamos armazenar os itens em uma lista de namedtuple
    
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
            
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))
        
    return capacity, item_count, items