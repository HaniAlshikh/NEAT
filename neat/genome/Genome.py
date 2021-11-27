import random

from neat.data_structure.ArraySet import ArraySet
from neat.genome.ConnectionGene import ConnectionGene
from neat.nn.NeuralNetwork import NeuralNetwork

class Genome:
    def __init__(self, neat):
        self.connections = ArraySet()
        self.nodes = ArraySet()
        self.neat = neat
        self.specie = None
        self.score = 0
        self.nn = None

    def activate(self, *input_nodes_inputs):
        if self.nn is None:
            self.generate_nn()
        return self.nn.activate(*input_nodes_inputs)

    def generate_nn(self):
        self.nn = NeuralNetwork.of_genome(self)

    # calculated the distance between this genome g1 and a second genome g2
    #  - g1 must have the highest innovation number!
    def distance(self, g2):
        g1 = self

        # TODO: genome with no connections?
        highest_innovation_g1 = g1.get_connections_highest_innovation_number()
        highest_innovation_g2 = g2.get_connections_highest_innovation_number()

        #  - g1 must have the highest innovation number!
        if highest_innovation_g1 < highest_innovation_g2:
            g1, g2 = g2, g1

        index_g1 = 0
        index_g2 = 0

        disjoint = 0
        weight_diff = 0
        similar = 0

        while index_g1 < g1.connections.size() and index_g2 < g2.connections.size():

            connection_gene1 = g1.connections.get(index_g1)
            connection_gene2 = g2.connections.get(index_g2)
            in1 = connection_gene1.innovation_number
            in2 = connection_gene2.innovation_number

            if in1 == in2:
                # similar connection genes
                similar += 1
                weight_diff += abs(connection_gene1.weight - connection_gene2.weight)
                index_g1 += 1
                index_g2 += 1
            elif in1 > in2:
                # disjoint connection gene of b
                disjoint += 1
                index_g2 += 1
            else:
                # disjoint connection gene of a
                disjoint += 1
                index_g1 += 1

        weight_diff /= max(1, similar)
        excess = g1.connections.size() - index_g1

        n = max(g1.connections.size(), g2.connections.size(), 1)
        return self.neat.C1 * disjoint / n + self.neat.C2 * excess / n + self.neat.C3 * weight_diff

        # n = max(g1.connections.size(), g2.connections.size())
        # if n < 20:
        #     n = 1
        #
        # return self.neat.C1 * disjoint / n + self.neat.C2 * excess / n + self.neat.C3 * weight_diff / n

    # creates a new genome.
    # g1 should have the higher score
    #  - take all the genes of a
    #  - if there is a genome in a that is also in b, choose randomly
    #  - do not take disjoint genes of b
    #  - take excess genes of a if they exist
    @staticmethod
    def cross_over(g1, g2):
        Genome.check_genes_sorting(g1, g2)

        neat = g1.neat
        genome = neat.get_empty_genome()

        index_g1 = 0
        index_g2 = 0

        while index_g1 < g1.connections.size() and index_g2 < g2.connections.size():

            connection_gene1 = g1.connections.get(index_g1)
            connection_gene2 = g2.connections.get(index_g2)
            in1 = connection_gene1.innovation_number
            in2 = connection_gene2.innovation_number

            if in1 == in2:
                con_gene = connection_gene1 if random.random() > 0.5 else connection_gene2
                genome.connections.add(con_gene.copy())
                index_g1 += 1
                index_g2 += 1
            elif in1 > in2:
                # disjoint gene of b
                genome.connections.add(connection_gene2.copy())
                index_g2 += 1
            else:
                # disjoint gene of a
                genome.connections.add(connection_gene1.copy())
                index_g1 += 1

        # add access connection genes
        while index_g1 < g1.connections.size():
            access_con_gene = g1.connections.get(index_g1)
            genome.connections.add(access_con_gene.copy())
            index_g1 += 1

        for con_gene in genome.connections:
            genome.nodes.add(con_gene.frm)
            genome.nodes.add(con_gene.to)

        return genome

    def mutate(self):
        if self.neat.PROBABILITY_MUTATE_CONNECTION > random.random():
            self.mutate_connection()
        elif self.neat.PROBABILITY_MUTATE_NODE > random.random():
            self.mutate_node()
        elif self.neat.PROBABILITY_MUTATE_SHIFT_WEIGHT > random.random():
            self.mutate_shift_weight()
        elif self.neat.PROBABILITY_MUTATE_RANDOM_WEIGHT > random.random():
            self.mutate_random_weight()
        elif self.neat.PROBABILITY_MUTATE_CONNECTION_TOGGLE > random.random():
            self.mutate_toggle_connection()

    def mutate_connection(self):
        # max 100 tries
        for i in range(100):
            a = self.nodes.get_random_element()
            b = self.nodes.get_random_element()
            if a is None or b is None: continue

            # avoid recursion and same layer nodes
            if a.x == b.x: continue

            neu_con = ConnectionGene(a, b) if a.x < b.x else ConnectionGene(b, a)
            # skip known connections
            if self.connections.contains(neu_con): continue

            # inform neat about the new connection to get an innovation number
            frm = neu_con.frm
            to = neu_con.to
            neu_con = self.neat.get_connection_or_create(neu_con.frm, neu_con.to)
            neu_con.weight = random.random() * 2 - 1 * self.neat.WEIGHT_RANDOM_STRENGTH

            # add sorted according to innovation number
            self.connections.add_ordered(neu_con)
            return

    def mutate_node(self):
        con = self.connections.get_random_element()
        # in case the genome has no connections
        if con is None: return;

        frm = con.frm
        to = con.to

        # get or create a middle node
        replace_innovation_number = self.neat.get_replace_innovation_number(frm, to)
        # replace_innovation_number = -1
        if replace_innovation_number == -1:
            middle = self.neat.get_node_or_create()
            middle.x = (frm.x + to.x) / 2
            middle.y = (frm.y + to.y) / 2 + random.random() * 0.02
            self.neat.set_replace_innovation_number(frm, to, middle.innovation_number)
        else:
            middle = self.neat.get_node_or_create(i=replace_innovation_number)

        con_to_mid = self.neat.get_connection_or_create(frm, middle)
        con_frm_mid = self.neat.get_connection_or_create(middle, to)

        con_to_mid.weight = 1
        con_frm_mid.weight = con.weight
        con_frm_mid.setEnabled = con.enabled

        self.connections.remove(con)
        # self.connections.add(con_to_mid)
        # self.connections.add(con_frm_mid)
        self.connections.add_ordered(con_to_mid)
        self.connections.add_ordered(con_frm_mid)

        self.nodes.add(middle)

    def mutate_shift_weight(self):
        con = self.connections.get_random_element()
        if con is not None:
            con.weight = con.weight + (random.random() * 2 - 1) * self.neat.WEIGHT_SHIFT_STRENGTH

    def mutate_random_weight(self):
        con = self.connections.get_random_element()
        if con is not None:
            con.weight = (random.random() * 2 - 1) * self.neat.WEIGHT_RANDOM_STRENGTH

    def mutate_toggle_connection(self):
        con = self.connections.get_random_element()
        if con is not None:
            con.enabled = not con.enabled

    def get_connections_highest_innovation_number(self):
        highest_innovation_num = 0
        if self.connections.size() != 0:
            highest_innovation_num = self.connections.get_last().innovation_number
        return highest_innovation_num

    def get_input_nodes(self):
        return [node for node in self.nodes if node.x == self.neat.INPUTS_X]

    def get_output_nodes(self):
        return [node for node in self.nodes if node.x == self.neat.OUTPUTS_X]

    def __repr__(self):
        return "{}: {}".format(self.score, self.connections)

    @staticmethod
    def check_genes_sorting(*genes):
        for g in genes:
            last_inv = 0
            for con in g.connections:
                if last_inv <= con.innovation_number:
                    last_inv = con.innovation_number
                else:
                    raise ValueError(g, "is not sorted correctly")