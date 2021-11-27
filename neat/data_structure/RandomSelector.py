import random


class RandomSelector:

    def __init__(self):
        self.population = []
        self.scores = []
        self.total_score = 0

    def add(self, genome):
        self.population.append(genome)
        self.scores.append(genome.score)
        self.total_score += genome.score

    # return a random element with a probability bias to the elements with the heights score
    def get(self):
        v = random.random() * self.total_score
        s = 0
        for i, g in enumerate(self.population):
            s += self.scores[i]
            if s >= v:
                s = i
                break
        return random.choice(self.population[max(0, s):])

    def reset(self):
        self.population.clear()
        self.scores.clear()
        self.total_score = 0
