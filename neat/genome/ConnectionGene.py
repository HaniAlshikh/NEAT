import neat.Neat as Neat
from neat.genome.Gene import Gene


class ConnectionGene(Gene):

    def __init__(self, frm, to, innovation_number=-1):
        super().__init__(innovation_number)
        self.frm = frm
        self.to = to
        self.weight = 0
        self.enabled = True
        # indicates if this connection was node mutated
        # and save the node innovation number to use in other genomes
        self.replace_innovation_number = -1

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        cp = ConnectionGene(self.frm, self.to, self.innovation_number)
        cp.weight = self.weight
        cp.enabled = self.enabled
        cp.replace_innovation_number = self.replace_innovation_number
        return cp

    def __eq__(self, o):
        if not isinstance(o, ConnectionGene): return False
        return self.frm == o.frm and self.to == o.to

    def __hash__(self):
        """Overrides the default implementation"""
        return self.frm.innovation_number * Neat.MAX_NODES + self.to.innovation_number

    def __repr__(self):
        return "{} {}-{}->{} {}".format(self.innovation_number, self.frm, self.weight, self.to, self.enabled)

