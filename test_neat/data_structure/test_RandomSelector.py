from unittest import TestCase

from neat.Neat import Neat
from neat.data_structure.RandomSelector import RandomSelector


class TestRandomSelector(TestCase):
    def setup(self):
        self.neat = Neat(4, 1, 100)
        self.genomes = []
        self.total_score = 0
        for i in range(10):
            self.genomes.append(self.neat.get_empty_genome())
            self.genomes[i].score = self.genomes[max(0, i-1)].score * 1.3 + 10
            self.total_score += self.genomes[i].score

    def test_add(self):
        # [GIVEN]
        self.setup()

        # [WHEN]
        selector = RandomSelector()
        for g in self.genomes:
            selector.add(g)

        # [THEN]
        self.assertEqual(self.genomes, selector.population)
        self.assertEqual([g.score for g in self.genomes], selector.scores)
        self.assertEqual(self.total_score, selector.total_score)

    def test_get(self):
        # [GIVEN]
        self.setup()
        selector = RandomSelector()
        for g in self.genomes:
            selector.add(g)

        # [WHEN]
        g = selector.get()

        # [THEN]
        self.assertIsNotNone(g)

    def test_reset(self):
        # [GIVEN]
        self.setup()
        selector = RandomSelector()
        for g in self.genomes:
            selector.add(g)

        # [WHEN]
        selector.reset()

        # [THEN]
        self.assertEqual(0, len(selector.population))
        self.assertEqual(0, len(selector.scores))
        self.assertEqual(0, selector.total_score)
