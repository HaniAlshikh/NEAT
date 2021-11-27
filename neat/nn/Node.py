import math


def sigmoid(weighted_sum):
    return 1 / (1 + math.exp(-weighted_sum))


def tanh(weighted_sum):
    return math.tanh(weighted_sum)


class Node:
    def __init__(self, a):
        self.a = a
        self.output = 0
        self.connections = []

    def calculate(self):
        self.output = tanh(self.get_weighted_sum())

    def get_weighted_sum(self):
        s = 0
        for con in self.connections:
            if con.enabled:
                s += con.weight * con.frm.output
        return s
    
    def __eq__(self, o):
        return self.a == o.a

    def __ne__(self, o):
        return self.a != o.a

    def __lt__(self, o):
        return self.a < o.a

    def __le__(self, o):
        return self.a <= o.a

    def __gt__(self, o):
        return self.a > o.a

    def __ge__(self, o):
        return self.a >= o.a