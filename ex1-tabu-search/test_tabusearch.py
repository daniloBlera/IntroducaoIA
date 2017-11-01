#!/usr/bin/env python3
# -*- coding: utf-8
import os
import random
from unittest import TestCase

from tabumain import *


class TestFunctions(TestCase):
    def test_mutation(self):
        walk = list(range(5))

        self.assertEqual(get_mutation_from(walk, 0), [1,0,2,3,4])
        self.assertEqual(get_mutation_from(walk, 1), [0,2,1,3,4])
        self.assertEqual(get_mutation_from(walk, 2), [0,1,3,2,4])
        self.assertEqual(get_mutation_from(walk, 3), [0,1,2,4,3])
        self.assertEqual(get_mutation_from(walk, 4), [4,1,2,3,0])

    def test_mutation_pool(self):
        walk = list(range(5))
        pool = get_pool_from(walk)

        expected = [
                [1,0,2,3,4],
                [0,2,1,3,4],
                [0,1,3,2,4],
                [0,1,2,4,3],
                [4,1,2,3,0],
                ]

        for i in range(len(walk)):
            self.assertEqual(pool[i], expected[i])

