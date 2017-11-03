#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import numpy as np


class SimpleFIFO:
    def __init__(self, max_length):
        assert max_length > 0, 'ERROR: List length must be greater than zero.'
        self.__max_length = max_length
        self.__elements = []

    def push(self, element):
        self.__elements.append(element)

        if len(self.__elements) > self.__max_length:
            del self.__elements[0]

    @property
    def MAX_LENGTH(self):
        return self.__max_length

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__elements

    def __len__(self):
        return str(len(self.__elements))

    def __getitem__(self, index):
        if index > len(self.__elements):
            raise IndexError(
                    'Índice maior ou igual ao comprimento da sequencia')

        return self.__elements[index]


def get_coordinates_from(data_path):
    """Retorna a lista de coordenadas das arestas.

    Lê o arquivo passado como argumento e retorna as coordenadas de todas as
    arestas por meio de um array no formato

        [['x_1', 'y_1'], ['x_2', 'y_2'], ..., ['x_n', 'y_n']]

    onde o i-ésimo par da lista corresponde às coordenadas da i-ésima aresta.

    Arg:
        data_path (str): Endereço do arquivo de dados.

    Returns:
       [[str, str]]: Lista de pares de coordenadas das arestas.
    """
    coordinates = []

    with open(data_path, 'r') as input_file:
        input_lines = input_file.read().strip(os.linesep).split(os.linesep)

        for i in range(len(input_lines)):
            if input_lines[i] == 'NODE_COORD_SECTION':
                coordinates = [row.split(' ')[1:] for row in input_lines[i+1:]]

    return coordinates


def get_cost_matrix_from(coordinates):
    """Obtém a matriz de custos entre as arestas.

    Dada uma lista de N arestas em R^2 de um grafo completo, retorna um ndarray 
    de formato (N x N) contendo os custos entre cada dois nós adjacentes

        | C_11 C_12 ... C_1N |   Onde:
        | C_21 C_22 ... C_2N |   * 'C_ij' é o valor do custo do passeio da
        |  .    .         .  |      aresta 'i' para 'j';
        |  .    .         .  |   *  C_ii = 0;
        |  .    .         .  |   *  C_ij = C_ji;
        | C_N1 C_N2 ... C_NN |

    Arg:
        coordinates ([['str', 'str']]): lista de coordenadas em R^2.

    Returns:
        numpy.ndarray: Matriz de custos entre arestas do grafo completo.
    """
    coord = np.asarray(coordinates, dtype=np.float32)
    num_edges = coord.shape[0]

    matrix = [np.linalg.norm(r1-r2) for r1 in coord for r2 in coord]
    return np.asarray(matrix).reshape((num_edges, num_edges))


def get_mutation_from(walk, index):
    """Obtém a mutação do passeio.

    Retorna o resultado obtido pela mutação do caminho aplicada entre as
    posições 'i' e 'i+1'.

    Example:
        Dado um caminho '[1,2,3,4,5]', a aplicação da mutação em index = 2
        resulta no caminho '[1,2,4,3,5]'.

    Args:
        walk ([int]): Sequência de arestas visitadas do passeio.
        inded(int): Posição em que a mutação deve ser aplicada.
    """
    mutation = walk[:]
    edges_num = len(mutation)
    aux = mutation[index]

    mutation[index] = mutation[(index+1) % edges_num]
    mutation[(index+1) % edges_num] = aux

    return mutation


def get_pool_from(walk):
    """Obtém uma lista de mutações.

    Retorna uma lista contendo os resultados da aplicação da operação de mutação
    'swap' entre as arestas 'i' e 'i+1', iterativamente da segunda à penúltima aresta
    do caminho enquanto o primeiro elemento é mantido fixo durante o processo, ou
    seja, dado o caminho

        [1,2,3,4,5]

    a função 'get_pool_from' retorna a lista de mutações

        [1,3,2,4,5] -- resultado da mutação [1,|2,3|,4,5] -> [1,|3,2|,4,5]
        [1,2,4,3,5] -- resultado da mutação [1,2,|3,4|,5] -> [1,2,|4,3|,5]
        [1,2,3,5,4] -- resultado da mutação [1,2,3,|4,5|] -> [1,2,3,|5,4|]

    Note que diferentemente do processo de mutação normalmente aplicado aos pares
    de arestas (1,2), (2,3), ..., (N-1, N), (N,0), onde N é o comprimento do caminho,
    nesta função a mutação é aplicada aos pares (2,3), (4,5), ..., (N-1, N).

    Arg:
        walk [int]: Lista de arestas visitadas.

    Returns:
        [[int]]: Lista de mutações do caminho original.
    """
    num_edges = len(walk)
    pool = []

    for i in range(1, num_edges - 1):
        mutation = get_mutation_from(walk, i)
        pool.append(mutation)

    return pool


def get_pool_from_ALT(walk):
    """Obtém uma lista de mutações.

    Retorna uma lista contendo os resultados da aplicação da operação de mutação
    'swap' entre as arestas 'i' e '(i+1) mod n' ou seja, dado o caminho

        [1,2,3,4,5]

    a função 'get_pool_from' retorna a lista de mutações

        [2,1,3,4,5] -- resultado da mutação [>1,2<,3,4,5] -> [>2,1<,2,4,5]
        [1,3,2,4,5] -- resultado da mutação [1,>2,3<,4,5] -> [1,>3,2<,4,5]
        [1,2,4,3,5] -- resultado da mutação [1,2,>3,4<,5] -> [1,2,>4,3<,5]
        [1,2,3,5,4] -- resultado da mutação [1,2,3,>4,5<] -> [1,2,3,>5,4<]
        [5,2,3,4,1] -- resultado da mutação [1<,2,3,4,>5] -> [5<,2,3,4,>1]

    Arg:
        walk [int]: Lista de arestas visitadas.

    Returns:
        [[int]]: Lista de mutações do caminho original.
    """
    num_edges = len(walk)
    pool = []

    for i in range(num_edges):
        mutation = get_mutation_from(walk, i)
        pool.append(mutation)

    return pool


def get_cost_of(walk, cost_matrix):
    """Calcula o custo do passeio completo.

    Args:
        walk:   Sequência de arestas visitadas do passeio.
        costs:  Matriz de custos entre as arestas.

    Returns:
        float:  Soma dos custos entre as arestas adjacentes.
    """
    edge_num = len(walk)
    cost = 0

    for i in range(edge_num):
        origin = walk[i]
        destiny = walk[(i+1) % edge_num]

        cost += cost_matrix[origin, destiny]

    return cost


def compact_form_of(walk):
    """A nicer format for printing."""
    string_form = [str(e) for e in walk]
    return '-'.join(string_form)

