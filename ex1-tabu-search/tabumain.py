#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import sys

import numpy as np


#  np.random.seed(1)


def get_coordinates_from(data_path):
    coordinates = []

    with open(data_path, 'r') as input_file:
        input_lines = input_file.read().strip(os.linesep).split(os.linesep)

        for i in range(len(input_lines)):
            if input_lines[i] == 'NODE_COORD_SECTION':
                coordinates = [row.split(' ')[1:] for row in input_lines[i+1:]]

    return coordinates


def euclidean_dist(p1, p2):
    return (np.sum((p1 - p2) ** 2)) ** (1/2)


def get_cost_matrix_from(coordinates):
    coord = np.asarray(coordinates, dtype=np.float32)
    num_edges = coord.shape[0]

    matrix = [euclidean_dist(r1, r2) for r1 in coord for r2 in coord]
    return np.asarray(matrix).reshape((num_edges, num_edges))


def get_mutation_from(individual, index):
    mutation = individual[:]
    aux = mutation[index]
    mutation[index] = mutation[(index+1) % 5]
    mutation[(index+1) % 5] = aux
    
    return mutation


def get_pool_from(individual):
    num_edges = len(individual)
    pool = [None] * num_edges

    for i in range(num_edges):
        pool[i] = get_mutation_from(individual, i)

    return pool


def main(data_path, iterations):
    coordinates = get_coordinates_from(data_path)
    costs = get_cost_matrix_from(coordinates)
    num_edges = len(coordinates)

    individual = list(range(num_edges))
    np.random.shuffle(individual)

    # TODO: Implementar lista tabu

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

