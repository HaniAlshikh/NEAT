from unittest import TestCase

from neat.Neat import Neat
from neat.genome.Specie import Specie


class TestSpecie(TestCase):
    def test_add(self):
        # [GIVEN]
        neat = Neat(2, 2, 100)
        g1 = neat.get_empty_genome()
        g2 = neat.get_empty_genome()
        g3 = neat.get_empty_genome()
        specie = Specie(g1)

        # [WHEN]
        specie.add(g2)
        specie.add(g3)

        # [THEN]
        self.assertEqual(3, specie.size())
        self.assertIsNotNone(g1.specie)
        self.assertIsNotNone(g2.specie)
        self.assertIsNotNone(g3.specie)
        self.assertEqual(specie.genomes.get(0), g1)
        self.assertEqual(specie.genomes.get(1), g2)
        self.assertEqual(specie.genomes.get(2), g3)

    def test_force_add(self):
        # [GIVEN]
        neat = Neat(2, 2, 100)
        g1 = neat.get_empty_genome()
        g2 = neat.get_empty_genome()
        g3 = neat.get_empty_genome()
        specie = Specie(g1)

        # [WHEN]
        specie.force_add(g2)
        specie.force_add(g3)

        # [THEN]
        self.assertEqual(3, specie.size())
        self.assertIsNotNone(g1.specie)
        self.assertIsNotNone(g2.specie)
        self.assertIsNotNone(g3.specie)
        self.assertEqual(specie.genomes.get(0), g1)
        self.assertEqual(specie.genomes.get(1), g2)
        self.assertEqual(specie.genomes.get(2), g3)

    def test_go_extinct(self):
        # [GIVEN]
        neat = Neat(2, 2, 100)
        g1 = neat.get_empty_genome()
        g2 = neat.get_empty_genome()
        g3 = neat.get_empty_genome()
        specie = Specie(g1)
        specie.add(g2)
        specie.add(g3)

        # [WHEN]
        specie.go_extinct()

        # [THEN]
        self.assertIsNone(g1.specie)
        self.assertIsNone(g2.specie)
        self.assertIsNone(g3.specie)

    def test_evaluate_score(self):
        self.fail()

    def test_reset(self):
        # [GIVEN]
        neat = Neat(2, 2, 100)
        g1 = neat.get_empty_genome()
        g2 = neat.get_empty_genome()
        g3 = neat.get_empty_genome()
        specie = Specie(g1)
        specie.add(g2)
        specie.add(g3)

        # [WHEN]
        specie.reset()

        # [THEN]
        none_count = 0
        for g in [g1, g2, g3]:
            if g.specie is None:
                none_count += 1
        self.assertEqual(2, none_count)
        self.assertIsNotNone(specie.representative.specie)
        self.assertTrue(specie.representative in [g1, g2, g3])

    def test_kill(self):
        # [GIVEN]
        neat = Neat(2, 2, 100)
        g1 = neat.get_empty_genome()
        g2 = neat.get_empty_genome()
        g3 = neat.get_empty_genome()
        specie = Specie(g1)
        specie.add(g2)
        specie.add(g3)
        g_with_max_score = g1
        for g in [g1, g2, g3]:
            if g.score > g_with_max_score.score:
                g_with_max_score = g

        # [WHEN]
        specie.kill(0.75)

        # [THEN]
        self.assertEqual(1, specie.genomes.size())
        none_count = 0
        for g in [g1, g2, g3]:
            if g.specie is None:
                none_count += 1
        self.assertEqual(2, none_count)
        self.assertEqual(specie.representative, g_with_max_score)

    def test_breed(self):
        self.fail()
