#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import numpy as np
from tabusearch import *


HANDLER = logging.StreamHandler()
HANDLER.setLevel(logging.DEBUG)

LOGGER = logging.getLogger('tabusearch-module-logger')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(HANDLER)


def translate(numbers):
    code = ['A','B','C','D','E']
    return [code[i] for i in numbers]


def translate_pair(number_costs):
    code = ['A','B','C','D','E']
    numbers, cost = number_costs
    #  text = [code[i] for i in numbers]
    text = translate(numbers)

    return (text, cost)


def debugging_run():
    """Execução do algoritmo com os parâmetros dos slides."""
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
    LOGGER.setLevel(logging.DEBUG)
    print('--RUNNING DEBUG--')
    debugging_run()
    print('--DEBUG RUN ENDED--')

