import operator

from neat.data_structure.ArraySet import ArraySet
from neat.genome.Genome import Genome


class Specie:
    def __init__(self, representative):
        self.representative = representative
        self.representative.species = self
        self.genomes = ArraySet()
        self.add(representative)
        self.score = 0

    def add(self, g):
        if g.distance(self.representative) < self.representative.neat.DT:
            self.force_add(g)
            return True
        return False

    def force_add(self, g):
        g.specie = self
        self.genomes.add(g)

    def go_extinct(self):
        for g in self.genomes:
            g.specie = None

    def evaluate_score(self):
        ss = 0
        for g in self.genomes:
            ss += g.score
        self.score = ss / self.genomes.size()

    def reset(self):
        representative = self.genomes.get_random_element()
        for g in self.genomes:
            g.specie = None
        self.genomes.clear()
        self.representative = representative
        self.representative.specie = self
        self.add(representative)
        self.score = 0

    def kill(self, percentage):
        self.genomes.sort('score')
        amount = int(percentage * self.genomes.size())
        for i in range(amount):
            self.genomes.get(0).specie = None
            self.genomes.remove(0)

    def breed(self):
        g1 = self.genomes.get_random_element()
        g2 = self.genomes.get_random_element()

        if g1.score > g2.score:
            return Genome.cross_over(g1, g2)

        return Genome.cross_over(g2, g1)

    def size(self):
        return self.genomes.size()

    def __repr__(self):
        return "{} {} {}".format(id(self), self.score, self.size())

