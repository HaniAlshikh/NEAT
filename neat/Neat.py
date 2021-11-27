from neat.data_structure.ArraySet import ArraySet
from neat.data_structure.RandomSelector import RandomSelector
from neat.genome.ConnectionGene import ConnectionGene
from neat.genome.Genome import Genome
from neat.genome.NodeGene import NodeGene
from neat.genome.Specie import Specie


class Neat:
    MAX_NODES = 2 ** 20
    C1 = C2 = C3 = 1
    DT = 4  # distance threshold compatibility threshold

    WEIGHT_SHIFT_STRENGTH = 0.3
    WEIGHT_RANDOM_STRENGTH = 1

    KILLING_RATE = 0.2

    PROBABILITY_MUTATE_CONNECTION = 0.01
    PROBABILITY_MUTATE_NODE = 0.1
    PROBABILITY_MUTATE_SHIFT_WEIGHT = 0.02
    PROBABILITY_MUTATE_RANDOM_WEIGHT = 0.02
    PROBABILITY_MUTATE_CONNECTION_TOGGLE = 0

    INPUTS_X = 0.1
    OUTPUTS_X = 0.9

    def __init__(self, inputs_count, outputs_count, genomes_count):
        self.reset(inputs_count, outputs_count, genomes_count)

    def reset(self, inputs_count, outputs_count, genomes_count):
        if inputs_count <= 0 or outputs_count <= 0 or genomes_count <= 0:
            raise ValueError(inputs_count, outputs_count, genomes_count, "are invalid constructor parameter")

        self.inputs_count = inputs_count
        self.outputs_count = outputs_count
        self.genomes_count = genomes_count

        self.connections = ArraySet()
        self.nodes = ArraySet()
        self.genomes = ArraySet()
        self.species = ArraySet()

        for i in range(inputs_count):
            self.get_node_or_create(x=self.INPUTS_X, y=(i) / float(inputs_count))

        for i in range(outputs_count):
            self.get_node_or_create(x=self.OUTPUTS_X, y=(i) / float(outputs_count))

        for i in range(genomes_count):
            g = self.get_empty_genome()
            # fully connected
            # for i in range(inputs_count):
            #     g.mutate_connection()
            #     g.mutate_random_weight()
            g.mutate()
            self.genomes.add(g)

    def evolve(self):
        self.gen_species()
        self.kill()
        self.remove_extinct_species()
        self.reproduce()
        self.mutate()
        for g in self.genomes:
            g.generate_nn()

    def gen_species(self):
        # release all genomes except representative
        for s in self.species:
            s.reset()

        for g in self.genomes:
            # skip representative
            if g.specie is not None:
                continue

            found_specie_for_genome = False
            for s in self.species:
                if s.add(g):
                    found_specie_for_genome = True
                    break

            # if not found create a new specie
            if not found_specie_for_genome:
                self.species.add(Specie(g))

        for s in self.species:
            s.evaluate_score()

    def kill(self):
        for s in self.species:
            s.kill(self.KILLING_RATE)

    def remove_extinct_species(self):
        # iterate downwards as the list is modified while iterating
        for i in range(self.species.size() - 1, -1, -1):
            s = self.species.get(i)
            if s.size() <= 1:
                s.go_extinct()
                self.species.remove(i)

    def reproduce(self):
        if self.species.isempty():
            self.gen_species()

        selector = RandomSelector()
        for s in self.species:
            selector.add(s)

        for g in self.genomes:
            if g.specie is None:
                specie = selector.get()
                g = specie.breed()
                specie.force_add(g)

    def mutate(self):
        for g in self.genomes:
            g.mutate()

    def get_empty_genome(self):
        g = Genome(self)
        for i in range(self.inputs_count + self.outputs_count):
            g.nodes.add(self.get_node_or_create(i))
        return g

    def get_node_or_create(self, i=-1, x=0.0, y=0.0):
        if not self.nodes.isempty() and 0 <= i < self.nodes.size():
            return self.nodes.get(i)
        n = NodeGene(self.nodes.size(), x, y)
        self.nodes.add(n)
        return n

    # the main connection object is saved in neat
    # and each genome should get a copy
    def get_connection_or_create(self, frm, to):
        new_con = ConnectionGene(frm, to)

        for connection in self.connections:
            if connection == new_con:
                return connection.copy()

        new_con.innovation_number = self.connections.size()
        self.connections.add(new_con)

        return new_con.copy()

    # def get_connection_or_create(self, frm, to):
    #     new_con = ConnectionGene(frm, to)
    #
    #     for connection in self.connections:
    #         if connection == new_con:
    #             new_con.innovation_number = connection.innovation_number
    #             break
    #
    #     if new_con.innovation_number == -1:
    #         new_con.innovation_number = self.connections.size()
    #         self.connections.add(new_con)
    #
    #     return new_con

    def get_elite(self):
        elite = self.genomes.get(0)
        for g in self.genomes:
            if g.score > elite.score:
                elite = g
        return elite

    def get_replace_innovation_number(self, frm, to):
        con = ConnectionGene(frm, to)
        con_in_neat = self.connections.get(con)
        if con_in_neat is None:
            return 0
        return con_in_neat.replace_innovation_number

    def set_replace_innovation_number(self, frm, to, innovation_number):
        self.connections.get(ConnectionGene(frm, to)).replace_innovation_number = innovation_number

    def print_species(self):
        print("##########################################")
        for s in self.species:
            print(s)
