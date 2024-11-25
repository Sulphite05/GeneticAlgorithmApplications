import random


def random_chromosome(num_of_queens):
    return [random.randint(1, num_of_queens) for _ in range(num_of_queens)]


def fitness(chromosome):
    horizontal_collisions = sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2

    n = len(chromosome)
    left_diagonal = [0] * (2 * n - 1)
    right_diagonal = [0] * (2 * n - 1)
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))  # 28-(2+3)=23


def probability(chromosome):
    return fitness(chromosome) / maxFitness


def random_pick(population, probabilities):
    total = sum(probabilities)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w


def reproduce(x, y):  # cross_over between two chromosomes
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]


def mutate(x):  # randomly changing the value of a random index of a chromosome
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x


def genetic_queen(population):
    mutation_probability = 0.03
    new_population = []
    probabilities = [probability(n) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities)  # best chromosome 1
        y = random_pick(population, probabilities)  # best chromosome 2
        child = reproduce(x, y)  # creating two new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            child = mutate(child)
        print_chromosome(child)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    return new_population


def print_chromosome(chrom):
    print(f"Chromosome = {chrom},  Fitness = {fitness(chrom)}")


if __name__ == "__main__":
    num_of_queens = int(input("Enter Number of Queens: "))
    if num_of_queens < 0 or num_of_queens == 2 or num_of_queens == 3:
        print(f"No solution for n = {num_of_queens}")
    else:
        maxFitness = (num_of_queens * (num_of_queens - 1)) / 2  # if num_of_queens = 8, 8*7/2 = 28
        population = [random_chromosome(num_of_queens) for _ in range(100)]

        generation = 1

        while generation < 1000 and not maxFitness in [fitness(chrom) for chrom in population]:
            print(f"=== Generation {generation} ===")
            population = genetic_queen(population)
            print()
            print(f"Maximum Fitness = {max([fitness(n) for n in population])}")
            generation += 1

        if generation == 1000:
            print("Generations crossed 1000! Repeat the process.")

        else:
            chrom_out = []
            print(f"Solved in Generation {generation - 1}")
            for chrom in population:
                if fitness(chrom) == maxFitness:
                    print("")
                    print("One of the solutions: ")
                    chrom_out = chrom
                    print_chromosome(chrom)

            board = []

            for x in range(num_of_queens):
                board.append(["x"] * num_of_queens)

            for i in range(num_of_queens):
                board[chrom_out[i]-1][i] = "Q"


            def print_board(board):
                for row in board:
                    print(" ".join(row))

            print()
            print_board(board)
