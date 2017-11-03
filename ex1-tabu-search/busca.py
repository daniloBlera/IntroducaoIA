#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

import numpy as np
from tabusearch import *

#  np.random.seed(1)

HANDLER = logging.StreamHandler()
HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger('tabusearch-module-logger')
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(HANDLER)

def main(data_path, iterations, max_tabu_length):
    coordinates = get_coordinates_from(data_path)
    costs = get_cost_matrix_from(coordinates)
    num_edges = len(coordinates)

    walk = list(range(1, num_edges))
    np.random.shuffle(walk)
    walk.insert(0,0)

    current_best = walk
    current_cost = get_cost_of(current_best, costs)

    tabu_list = SimpleFIFO(max_tabu_length)
    tabu_list.push(current_best)

    choice_historic = []

    for i in range(iterations):
        pool = get_pool_from(current_best)
        pool_costs = [(e, get_cost_of(e, costs)) for e in pool]
        pool_costs.sort(key=lambda p: p[1])

        tabu_list_costs = [get_cost_of(e, costs) for e in tabu_list]

        LOGGER.debug('--ITERAÇÃO: \'%d\'--', i)
        LOGGER.debug('--TABU LIST COSTS--')
        for e in tabu_list_costs:
            LOGGER.debug(e)

        sorted_costs = [e[1] for e in pool_costs]
        length = len(sorted_costs)
        print_range = 10 if length >= 10 else length

        LOGGER.debug('\n--FIRST %d SORTED COSTS (decreasing order)--', print_range)
        for ii in range(print_range):
            LOGGER.debug(sorted_costs[ii])

        for e in pool_costs:
            if e[0] in tabu_list:
                continue
            else:
                current_best = e[0]
                current_cost = get_cost_of(current_best, costs)
                tabu_list.push(current_best)
                break

        LOGGER.debug('\n--CHOOSEN WALK COST--\n%f\n', current_cost)

        choice_historic.append((current_best, current_cost))
        pool.clear()
        pool_costs.clear()

    LOGGER.info('...BUSCA CONCLUÍDA\n')
    LOGGER.info('--CAMINHO INICIAL (obtido aleatoriamente)--')
    LOGGER.critical('%s', compact_form_of(walk))

    LOGGER.info('\n--CAMINHO ENCONTRADO--')
    LOGGER.critical('%s', compact_form_of(current_best))

    LOGGER.info('\n--CUSTO--')
    LOGGER.critical('%f', current_cost)

    LOGGER.debug('--HISTORIC OF COSTS--')
    for i in range(len(choice_historic)):
        LOGGER.debug('ITERAÇÃO %d: %f', i, choice_historic[i][1])


def translate(numbers):
    code = ['A','B','C','D','E']
    return [code[i] for i in numbers]

def translate_pair(number_costs):
    code = ['A','B','C','D','E']
    numbers, cost = number_costs
    text = [code[i] for i in numbers]

    return (text, cost)

def debugging_run():
    get_pool_from = get_pool_from_ALT

    costs = [
                [0,2,4,5,3],
                [2,0,3,6,4],
                [4,3,0,5,5],
                [5,6,5,0,4],
                [3,4,5,4,0]
            ]

    costs = np.asarray(costs, dtype=np.float32)
    walk = [1,4,3,2,0] # [B,E,D,C,A]
    num_edges = 5

    current_best = walk
    current_cost = get_cost_of(current_best, costs)

    tabu_list = SimpleFIFO(5)
    tabu_list.push(current_best)

    for i in range(3):
        pool = get_pool_from(current_best)
        pool_costs = [(e, get_cost_of(e, costs)) for e in pool]

        LOGGER.debug('\n--ITERAÇÃO: %d--', i+1)
        LOGGER.debug('--POOL AND COSTS--')
        for e in pool_costs:
            LOGGER.debug('%s', translate_pair(e))

        tabu_list_costs = [get_cost_of(e, costs) for e in tabu_list]
        pool_costs.sort(key=lambda p: p[1])

        tabu_costs = [(e, get_cost_of(e, costs)) for e in tabu_list]

        LOGGER.debug('\n--TABU AND COSTS--')
        for e in tabu_costs:
            LOGGER.debug(translate_pair(e))

        for e in pool_costs:
            if e[0] in tabu_list:
                continue
            else:
                current_best = e[0]
                current_cost = get_cost_of(current_best, costs)
                tabu_list.push(current_best)
                break

        LOGGER.debug('\n--CHOOSEN WALK COST--\n%f\n', current_cost)

        pool.clear()
        pool_costs.clear()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('DATA', help='Caminho do arquivo de dados', type=str)
    parser.add_argument(
            '-i', help='Número de iterações', type=int)
    parser.add_argument(
            '-l',  help='Comprimento da lista tabu', type=int)
    parser.add_argument('-d', help='Habilitar modo depuração', action='store_true')
    parser.add_argument('-t', help='Executar caso de teste', action='store_true')
    parser.add_argument(
            '-o', help='Retornar caminho e custo apenas', action='store_true')

    args = parser.parse_args()

    iterations = 1000
    if args.i:
        iterations = args.i

    max_tabu_length = 5
    if args.l:
        max_tabu_length = args.l

    if args.d:
        LOGGER.setLevel(logging.DEBUG)

    if args.t:
        LOGGER.setLevel(logging.DEBUG)
        print('--RUNNING DEBUG--')
        debugging_run()
        print('--DEBUG RUN ENDED--')
        exit(0)

    if args.o:
        LOGGER.setLevel(logging.CRITICAL)

    LOGGER.info('TSP WITH TABU SEARCH\nARQUIVO: \'%s\'\n', args.DATA)
    LOGGER.info('BUSCANDO SOLUÇÃO...')
    main(args.DATA, iterations, max_tabu_length)

