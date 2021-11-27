from neat.genome.Gene import Gene


class NodeGene(Gene):

    def __init__(self, innovation_number=-1, x=0.0, y=0.0):
        super().__init__(innovation_number)
        self.x = x
        self.y = y

    def __eq__(self, o):
        if not isinstance(o, NodeGene):
            return False
        return self.innovation_number == o.innovation_number

    def __hash__(self):
        """Overrides the default implementation"""
        return self.innovation_number

    def __repr__(self):
        return "{}".format(self.innovation_number)
