from unittest import TestCase

from neat.GUI import Presenter
from neat.Neat import Neat
from neat.genome.ConnectionGene import ConnectionGene
from neat.genome.Genome import Genome
from neat.genome.NodeGene import NodeGene


class TestGenome(TestCase):
    def test_distance(self):
        # https://ai.stackexchange.com/questions/9550/how-does-the-neat-speciation-algorithm-work
        # [GIVEN]
        neat = Neat(4, 2, 1000)
        g1 = neat.get_empty_genome()
        g2 = neat.get_empty_genome()

        c1 = neat.get_connection_or_create(neat.get_node_or_create(0), neat.get_node_or_create(3))
        c2 = neat.get_connection_or_create(neat.get_node_or_create(1), neat.get_node_or_create(3))
        c3 = neat.get_connection_or_create(neat.get_node_or_create(2), neat.get_node_or_create(3))
        c4 = neat.get_connection_or_create(neat.get_node_or_create(1), neat.get_node_or_create(4))
        c5 = neat.get_connection_or_create(neat.get_node_or_create(2), neat.get_node_or_create(4))
        c6 = neat.get_connection_or_create(neat.get_node_or_create(3), neat.get_node_or_create(4))

        # [[1,.25][2,.55],[4,.78],[6,.2]]
        g1.connections.add(neat.get_connection_or_create(c1.frm, c1.to))
        g1.connections.add(neat.get_connection_or_create(c2.frm, c2.to))
        g1.connections.add(neat.get_connection_or_create(c4.frm, c4.to))
        g1.connections.add(neat.get_connection_or_create(c6.frm, c6.to))

        g1.connections.get(c1).weight = 25
        g1.connections.get(c2).weight = 55
        g1.connections.get(c4).weight = 78
        g1.connections.get(c6).weight = 2

        # [[1,.15][3,.92],[5,.37]]
        g2.connections.add(neat.get_connection_or_create(c1.frm, c1.to))
        g2.connections.add(neat.get_connection_or_create(c3.frm, c3.to))
        g2.connections.add(neat.get_connection_or_create(c5.frm, c5.to))

        g2.connections.get(c1).weight = 15
        g2.connections.get(c3).weight = 92
        g2.connections.get(c5).weight = 37

        # [WHEN]
        d = g1.distance(g2)

        # [THEN]
        # E access, D = disjoint, W average weight differences of matching genes, N = number of connections
        # distance 𝛿 = c1*𝐸/𝑁 + c2*𝐷/𝑁 + c3*𝑊
        # 𝐸 = 1, 𝐷 = 4, 𝑊 = 10, c1,c2,c3 = 1, 𝑁 = 4
        # 𝛿 = 11.25
        self.assertEqual(11.25, d)


    def test_cross_over(self):
        # [GIVEN]
        neat = Neat(3, 1, 100)
        p1 = neat.get_empty_genome()
        p2 = neat.get_empty_genome()

        c1 = neat.get_connection_or_create(neat.get_node_or_create(0), neat.get_node_or_create(3))
        c2 = neat.get_connection_or_create(neat.get_node_or_create(1), neat.get_node_or_create(3))
        c3 = neat.get_connection_or_create(neat.get_node_or_create(2), neat.get_node_or_create(3))
        c4 = neat.get_connection_or_create(neat.get_node_or_create(1), neat.get_node_or_create(4))
        c5 = neat.get_connection_or_create(neat.get_node_or_create(2), neat.get_node_or_create(4))
        c6 = neat.get_connection_or_create(neat.get_node_or_create(3), neat.get_node_or_create(4))
        c7 = neat.get_connection_or_create(neat.get_node_or_create(0), neat.get_node_or_create(5))
        c8 = neat.get_connection_or_create(neat.get_node_or_create(5), neat.get_node_or_create(3))

        p1.connections.add(neat.get_connection_or_create(c1.frm, c1.to))
        p1.connections.add(neat.get_connection_or_create(c2.frm, c2.to))
        p1.connections.add(neat.get_connection_or_create(c4.frm, c4.to))
        p1.connections.add(neat.get_connection_or_create(c5.frm, c5.to))
        p1.connections.add(neat.get_connection_or_create(c6.frm, c6.to))

        p2.connections.add(neat.get_connection_or_create(c1.frm, c1.to))
        p2.connections.add(neat.get_connection_or_create(c2.frm, c2.to))
        p2.connections.add(neat.get_connection_or_create(c3.frm, c3.to))
        p2.connections.add(neat.get_connection_or_create(c4.frm, c4.to))
        p2.connections.add(neat.get_connection_or_create(c6.frm, c6.to))
        p2.connections.add(neat.get_connection_or_create(c7.frm, c7.to))
        p2.connections.add(neat.get_connection_or_create(c8.frm, c8.to))

        p1.connections.get(c4).enabled = False
        p2.connections.get(c1).enabled = False
        p2.connections.get(c4).enabled = False

        p2.score = 10
        p1.score = 5

        # [WHEN]
        offspring_p1_p2 = Genome.cross_over(p1, p2)
        offspring_p2_p1 = Genome.cross_over(p2, p1)

        # [THEN]
        c4.enabled = False
        self.assertListEqual([c1, c2, c3, c4, c5, c6], offspring_p1_p2.connections.get_data())
        c1.enabled = True  # randomly chosen in our case
        c4.enabled = False
        self.assertListEqual([c1, c2, c3, c4, c5, c6, c7, c8], offspring_p2_p1.connections.get_data())

    def test_mutate_connection(self):
        # [GIVEN]
        inputs_count = 2
        outputs_count = 4
        possible_connections = inputs_count * outputs_count
        neat = Neat(2, 4, 100)
        g1 = neat.get_empty_genome()
        g2 = neat.get_empty_genome()

        # [WHEN]
        # create all possible connection
        for i in range(100):
            g1.mutate_connection()
            g2.mutate_connection()
        # modify genome connections
        for g1_con, g2_con in zip(g1.connections, g2.connections):
            g1_con.weight = 10
            g2_con.enabled = False

        # [THEN]
        # all possible connections should be created
        self.assertEqual(possible_connections, g1.connections.size())
        self.assertEqual(possible_connections, g2.connections.size())
        self.assertEqual(possible_connections, neat.connections.size())
        # all connections are modified on genome based
        for g1_con, g2_con, neat_con in zip(g1.connections, g2.connections, neat.connections):
            self.assertEqual(10, g1_con.weight)
            self.assertFalse(g2_con.enabled)
            self.assertNotEqual(10, neat_con.weight)
            self.assertTrue(neat_con.enabled)
        # all connections are in neat but not the same object
        for con in neat.connections:
            self.assertTrue(con in g1.connections)
            self.assertTrue(con in g2.connections)
        # all connections have the same innovation number
        for con in neat.connections:
            self.assertIsInstance(g1.connections.get(con.innovation_number), ConnectionGene)
            self.assertIsInstance(g2.connections.get(con.innovation_number), ConnectionGene)
        # (checking one genome is sufficient now)
        # no connection between same nodes or same layer nodes
        for con in g1.connections:
            if con.frm in g1.get_input_nodes():
                self.assertTrue(con.to in g1.get_output_nodes())
            if con.frm in g1.get_output_nodes():
                self.assertTrue(con.to in g1.get_input_nodes())
        # insure sorted order according to the innovation number
        for i, con in enumerate(g1.connections):
            self.assertEqual(i, con.innovation_number)

    def test_mutate_node(self):
        # [GIVEN]
        inputs_count = 2
        outputs_count = 4
        possible_connections = inputs_count * outputs_count
        neat = Neat(2, 4, 100)
        g1 = neat.get_empty_genome()
        g2 = neat.get_empty_genome()
        g3 = neat.get_empty_genome()
        # g1 and g2 have a connection from and to the same node
        frm = neat.nodes.get(g1.get_input_nodes()[0])
        to = neat.nodes.get(g1.get_output_nodes()[0])
        con = neat.get_connection_or_create(frm, to)
        g1.connections.add(con.copy())
        g2.connections.add(con.copy())
        old_node_count = neat.nodes.size()
        old_con_count = neat.connections.size()

        # [WHEN]
        # mutate a node in g1
        g1.mutate_node() # old_node_count + 1
        g3.mutate_node() # old_node_count + 0 (has no connections)

        self.assertEqual(old_node_count + 1, neat.nodes.size())
        self.assertEqual(old_node_count + 1, g1.nodes.size())
        self.assertEqual(old_node_count, g2.nodes.size())
        self.assertEqual(old_node_count, g3.nodes.size())

        self.assertEqual(old_con_count + 2, neat.connections.size())  # frm_to, frm_mid, mid_to -> +2
        self.assertEqual(old_con_count + 1, g1.connections.size())  # frm_mid, mid_to -> +1
        self.assertEqual(old_con_count, g2.connections.size())  # frm_to -> +0
        self.assertEqual(0, g3.connections.size())  # has no connection

    def test_mutate_shift_weight(self):
        # [GIVEN]
        inputs_count = 2
        outputs_count = 4
        neat = Neat(inputs_count, outputs_count, 100)
        genome = neat.get_empty_genome()
        genome.mutate_connection()
        old_weight = genome.connections.get(0).weight

        # [WHEN]
        genome.mutate_shift_weight()

        # [THEN]
        self.assertNotEqual(old_weight, genome.connections.get(0).weight)

    def test_mutate_random_weight(self):
        # [GIVEN]
        inputs_count = 2
        outputs_count = 4
        neat = Neat(inputs_count, outputs_count, 100)
        genome = neat.get_empty_genome()
        genome.mutate_connection()
        old_weight = genome.connections.get(0).weight

        # [WHEN]
        genome.mutate_random_weight()

        # [THEN]
        self.assertNotEqual(old_weight, genome.connections.get(0).weight)

    def test_mutate_toggle_connection(self):
        # [GIVEN]
        inputs_count = 2
        outputs_count = 4
        neat = Neat(inputs_count, outputs_count, 100)
        genome = neat.get_empty_genome()
        genome.mutate_connection()

        # [WHEN]
        genome.mutate_toggle_connection()

        # [THEN]
        self.assertFalse(genome.connections.get(0).enabled)

    def test_get_connections_highest_innovation_number(self):
        # [GIVEN]
        inputs_count = 2
        outputs_count = 4
        neat = Neat(inputs_count, outputs_count, 100)
        genome = neat.get_empty_genome()
        con_count = 3
        for _ in range(3):
            genome.mutate_connection()

        # [WHEN]
        got = genome.get_connections_highest_innovation_number()

        # [THEN]
        self.assertEqual(con_count - 1, got)
