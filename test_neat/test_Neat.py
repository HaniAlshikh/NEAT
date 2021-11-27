from unittest import TestCase

from neat.Neat import Neat
from neat.genome.ConnectionGene import ConnectionGene
from neat.genome.NodeGene import NodeGene


class TestNeat(TestCase):

    def test_reset(self):
        # [GIVEN]
        # input_count, output_count, genome_count
        valid_tests = [
            (2, 3, 100, 5, "not matching counts"),
            (1, 1, 100, 2, "matching counts"),
        ]
        invalid_tests = [
            (0, 3, 100, ValueError, "no input nodes"),
            (3, 0, 100, ValueError, "no output nodes"),
            (-1, 2, 100, ValueError, "negative input nodes count"),
            (1, -2, 100, ValueError, "negative output nodes count"),
        ]

        for input_count, output_count, genome_count, expected, msg in valid_tests:
            with self.subTest(msg):
                # [WHEN]
                neat = Neat(input_count, output_count, genome_count)

                # [THEN]
                self.assertEqual(expected, neat.nodes.size())
                self.assertEqual(0, neat.connections.size())
                # self.assertEqual(genome_count, neat.genomes.size())

        for input_count, output_count, genome_count, expected, msg in invalid_tests:
            with self.subTest(msg):
                # [WHEN] [THEN]
                self.assertRaises(expected, Neat, input_count, output_count, genome_count)

    def test_empty_genome(self):
        # [GIVEN]
        # input_count, output_count, genome_count
        tests = [
            (2, 3, 100, 5, "not matching counts"),
            (1, 1, 100, 2, "matching counts"),
        ]

        for input_count, output_count, genome_count, expected, msg in tests:
            with self.subTest(msg):
                # [WHEN]
                neat = Neat(input_count, output_count, genome_count)
                genome = neat.get_empty_genome()

                # [THEN]
                self.assertEqual(expected, genome.nodes.size())

    def test_get_node_or_create(self):
        # [GIVEN]
        neat = Neat(2, 2, 100) # init 4 nodes
        existing_node = neat.get_node_or_create(0)
        new_node = NodeGene(4, 0, 0) # the 5th node

        # [WHEN]
        got_existing = neat.get_node_or_create(existing_node.innovation_number)
        got_new = neat.get_node_or_create(new_node.innovation_number, new_node.x, new_node.y)

        # [THEN]
        self.assertEqual(5, neat.nodes.size())
        self.assertEqual(got_existing, existing_node)
        self.assertEqual(got_new, new_node)

    def test_get_connection_or_create(self):
        # [GIVEN]
        neat = Neat(2, 2, 100) # init 4 nodes
        frm = neat.get_node_or_create(0)
        to = neat.get_node_or_create(2)
        new_con = ConnectionGene(frm, to)

        # [WHEN]
        got_new = neat.get_connection_or_create(frm, to)
        got_existing = neat.get_connection_or_create(frm, to)

        # [THEN]
        self.assertEqual(1, neat.connections.size())
        self.assertEqual(new_con, got_new)
        self.assertEqual(got_new, got_existing)
