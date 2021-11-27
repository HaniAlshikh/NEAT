from neat.genome import Genome
from neat.nn.Connection import Connection
from neat.nn.Node import Node


class NeuralNetwork:
    def __init__(self):
        self.input_nodes = []
        self.hidden_nodes = []
        self.output_nodes = []

    @staticmethod
    def of_genome(g: Genome):
        nn = NeuralNetwork()
        nodes = g.nodes
        cons = g.connections

        node_map = {}

        for n in nodes:
            node = Node(n.x)
            node_map[n.innovation_number] = node

            if n.x <= 0.1:
                nn.input_nodes.append(node)
            elif n.x >= 0.9:
                nn.output_nodes.append(node)
            else:
                nn.hidden_nodes.append(node)

        nn.hidden_nodes.sort(reverse=True) # descending

        for con_gene in cons:
            frm = con_gene.frm
            to = con_gene.to

            node_frm = node_map[frm.innovation_number]
            node_to = node_map[to.innovation_number]

            con = Connection(node_frm, node_to)
            con.weight = con_gene.weight
            con.enabled = con_gene.enabled

            node_to.connections.append(con)

        return nn

    def activate(self, *inputs_outputs):
        output = []

        if len(inputs_outputs) != len(self.input_nodes):
            raise ValueError("inputs doesn't match input nodes")

        for i, n in enumerate(self.input_nodes):
            n.output = inputs_outputs[i]

        for n in self.hidden_nodes:
            n.calculate()

        for i, n in enumerate(self.output_nodes):
            n.calculate()
            output.append(n.output)

        return output
