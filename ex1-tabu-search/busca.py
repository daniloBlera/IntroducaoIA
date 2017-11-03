#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

import numpy as np
from tabusearch import *


HANDLER = logging.StreamHandler(sys.stdout)
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
        LOGGER.debug('--LISTA TABU E COSTS--')
        for e in tabu_list_costs:
            LOGGER.debug(e)

        sorted_costs = [e[1] for e in pool_costs]
        length = len(sorted_costs)
        print_range = 10 if length >= 10 else length

        LOGGER.debug('\n--PRIMEIROS %d CUSTOS (ordenados)--', print_range)
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

        LOGGER.debug('\n--CUSTO DO CAMINHO ESCOLHIDO--\n%f\n', current_cost)

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

    LOGGER.debug('--HISTÓRICO DE CUSTOS--')
    for i in range(len(choice_historic)):
        LOGGER.debug('ITERAÇÃO %d: %f', i, choice_historic[i][1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('DATA', help='Caminho do arquivo de dados', type=str)
    parser.add_argument('-i', help='Número de iterações', type=int)
    parser.add_argument('-l',  help='Comprimento da lista tabu', type=int)
    parser.add_argument('-v', help='Habilitar modo verboso', action='store_true')
    parser.add_argument(
            '-o', help='Retornar caminho e custo apenas', action='store_true')
    parser.add_argument('-s', help='Valor do \'seed\'', type=int)

    args = parser.parse_args()

    if args.o:
        LOGGER.setLevel(logging.CRITICAL)

    LOGGER.info('TSP WITH TABU SEARCH\nARQUIVO: \'%s\'\n', args.DATA)
    LOGGER.info('--PARÂMETROS--')

    iterations = 100
    if args.i:
        iterations = args.i
    LOGGER.info('ITERAÇÕES: %d', iterations)

    max_tabu_length = 5
    if args.l:
        max_tabu_length = args.l
    LOGGER.info('COMPRIMENTO MÁXIMO DA LISTA TABU: %d', max_tabu_length)

    if args.v:
        LOGGER.setLevel(logging.DEBUG)

    if args.s:
        np.random.seed(args.s)
        LOGGER.info('SEED UTILIZADA: %d\n', args.s)

    LOGGER.info('BUSCANDO SOLUÇÃO...')
    main(args.DATA, iterations, max_tabu_length)

