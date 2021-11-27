import random
from unittest import TestCase

from neat.data_structure.ArraySet import ArraySet
from neat.genome.ConnectionGene import ConnectionGene
from neat.genome.NodeGene import NodeGene


class TestArraySet(TestCase):
    def test_add_ordered(self):
        # [GIVEN]
        cons = []
        for i in range(100):
            cons.append(ConnectionGene(NodeGene(), NodeGene(), i))
        random.shuffle(cons)
        for i in range(50):
            cons.pop()
        l = ArraySet()

        # [WHEN]
        for con in cons:
            l.add_ordered(con)

        # [THEN]
        last_inv = 0
        for con in l:
            self.assertLessEqual(last_inv, con.innovation_number)
            last_inv = con.innovation_number