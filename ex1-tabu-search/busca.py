#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys

import numpy as np
from tabusearch import *


def main(data_path, iterations, max_tabu_length):
    coordinates = get_coordinates_from(data_path)
    costs = get_cost_matrix_from(coordinates)
    num_edges = len(coordinates)
    
    walk = list(range(num_edges))
    np.random.shuffle(walk)

    current_best = walk
    current_cost = get_cost_of(current_best, costs)
    
    tabu_list = SimpleFIFO(max_tabu_length)
    tabu_list.insert(current_best)
    
    for i in range(iterations):
        pool = get_pool_from(walk)
        pool_costs = [(e, get_cost_of(e, costs)) for e in pool]
        pool_costs.sort(key=lambda p: p[1], reverse=True)

        for e in pool_costs:
            if e[0] in tabu_list:
                continue
            else:
                current_best = e[0]
                current_cost = get_cost_of(current_best, costs)
                tabu_list.insert(current_best)
                break

        pool.clear()
        pool_costs.clear()

    print('...CONCLUÍDO\n')
    print('CAMINHO ENCONTRADO')
    print('{0}\n\nCUSTO:{1}\n'.format(current_best, current_cost))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('DATA', help='Caminho do arquivo de dados', type=str)
    parser.add_argument(
            '-i', help='Número de iterações', type=int)
    parser.add_argument(
            '-l',  help='Comprimento da lista tabu', type=int)

    args = parser.parse_args()
    
    iterations = 1000
    if args.i:
        iterations = args.i
    
    max_tabu_length = 5
    if args.l:
        max_tabu_length = args.l

    print('TSP WITH TABU SEARCH\nARQUIVO: \'{}\'\n'.format(args.DATA))
    print('BUSCANDO SOLUÇÃO...')
    main(args.DATA, iterations, max_tabu_length)

