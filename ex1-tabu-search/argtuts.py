#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-f', help='File path', type=str)
parser.add_argument('-i', help='Number of iterations', type=int)
parser.add_argument('filepath', help='File path, obr', type=str)

args = parser.parse_args()
print(args)
print(args.filepath)
