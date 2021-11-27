import random
from neat.Neat import Neat


def main():
    input_count, output_count, genome_count = 10, 1, 100
    neat = Neat(input_count, output_count, genome_count)

    # Presenter.present(neat.get_empty_genome())

    input_nodes_outputs = []
    for _ in range(input_count):
        input_nodes_outputs.append(random.random())

    runs = 80
    for i in range(runs):
        for g in neat.genomes:
            score = g.activate(*input_nodes_outputs)[0]  # only one output
            g.score = score
        neat.evolve()
        neat.print_species()
        print("================== {} ======================".format(i))

    # for g in neat.genomes:
    #     for c in g.connections:
    #         print(c.innovation_number, end=' ')
    #     print()

    # Presenter.present(random.choice(neat.genomes.get_data()))


if __name__ == "__main__":
    main()
