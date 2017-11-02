#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import sys

import numpy as np


#  np.random.seed(1)


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


def euclidean_dist(p1, p2):
    """Calcula a distância euclidiana entre os pontos.

    Calcula o valor da distância d(p,q), onde

        d(p,q) = d(q,p) = Sqrt(Sum_i^n {p_i - q_i) ^ 2})

    ou em formato vetorial, sejam 'p' e 'q' vetores em R^n, temos

        d(p,q) = Sqrt((p - q) .* (p - q))
    
    onde '.*' é a operador do 'produto hadamard'.

    Args:
        p1 (numpy.ndarray): Ponto em R^n.
        p2 (numpy.ndarray): Ponto em R^n.

    Returns:
        float: Distância euclidiana entre p1 e p2.
    """
    return (np.sum((p1 - p2) ** 2)) ** (1/2)


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

    matrix = [euclidean_dist(r1, r2) for r1 in coord for r2 in coord]
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
    aux = mutation[index]
    mutation[index] = mutation[(index+1) % 5]
    mutation[(index+1) % 5] = aux
    
    return mutation


def get_pool_from(walk):
    """Obtém uma lista de mutações.
    
    Retorna uma lista contendo os resultados da aplicação de mutação entre todos
    os possíveis elementos adjacentes do caminho, ou seja, dado o caminho

        [1,2,3,4,5]

    retorna a lista de mutações

        [2,1,3,4,5]
        [1,3,2,4,5]
        [1,2,4,3,5]
        [1,2,3,5,4]
        [5,2,3,4,1]

    Arg:
        walk [int]: Lista de arestas visitadas.

    Returns:
        [[int]]: Lista de mutações do caminho original.
    """
    num_edges = len(walk)
    pool = [None] * num_edges

    for i in range(num_edges):
        pool[i] = get_mutation_from(walk, i)

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


def main(data_path, iterations):
    coordinates = get_coordinates_from(data_path)
    costs = get_cost_matrix_from(coordinates)
    num_edges = len(coordinates)
    
    walk = list(range(num_edges))
    np.random.shuffle(walk)
    tabu_list = [walk]

    for i in range(iterations):
        pool = get_pool_from(walk)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('DATA', help='Caminho do arquivo de dados', type=str)
    parser.add_argument(
            '-i', help='Número de iterações', type=int)
    parser.add_argument(
            '-l', '--length',  help='Comprimento da lista tabu', type=int)

    args = parser.parse_args()

    print("TSP WITH TABU SEARCH\nFILENAME: '{}'".format(args.DATA))
    
    iterations = 1000
    if args.i:
        iterations = args.i

    main(args.DATA, iterations)

