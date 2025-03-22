import random
from copy import deepcopy
from models.individual import Individual
from models.chromosome import Chromosome

def tournament_selection(population, tournament_size=3):
    """
    Selekcja turniejowa: z losowo dobranej grupy o rozmiarze tournament_size wybieramy najlepszego osobnika.
    :param population: instancja klasy Population
    :param tournament_size: liczba osobników w turnieju
    :return: lista wybranych osobników (długość równa rozmiarowi populacji)
    """
    selected = []
    pop = population.individuals
    for _ in range(len(pop)):
        tournament = random.sample(pop, tournament_size)
        best = min(tournament, key=lambda ind: ind.fitness)  # zakładamy minimalizację
        selected.append(best)
    return selected

def roulette_selection(population):
    """
    Selekcja ruletkowa dla problemu minimalizacji.
    Im mniejsza wartość fitness, tym większa szansa na wybór.
    :param population: instancja klasy Population
    :return: lista wybranych osobników (długość równa rozmiarowi populacji)
    """
    pop = population.individuals
    epsilon = 1e-6
    max_fitness = max(ind.fitness for ind in pop)
    total = sum(max_fitness - ind.fitness + epsilon for ind in pop)
    selected = []
    for _ in range(len(pop)):
        r = random.uniform(0, total)
        accumulator = 0
        for ind in pop:
            accumulator += max_fitness - ind.fitness + epsilon
            if accumulator >= r:
                selected.append(ind)
                break
    return selected

def best_selection(population, count):
    """
    Wybiera określoną liczbę najlepszych osobników.
    :param population: instancja klasy Population
    :param count: liczba najlepszych osobników do zwrócenia
    :return: lista najlepszych osobników
    """
    sorted_individuals = sorted(population.individuals, key=lambda ind: ind.fitness)
    return sorted_individuals[:count]

def one_point_crossover(parent1: Individual, parent2: Individual):
    """
    Krzyżowanie jednopunktowe.
    Zakłada, że oba rodzice mają chromosomy o tej samej długości.
    :param parent1: pierwszy rodzic (Individual)
    :param parent2: drugi rodzic (Individual)
    :return: para nowych osobników potomnych
    """
    gene1 = parent1.chromosome.gene
    gene2 = parent2.chromosome.gene
    if len(gene1) != len(gene2):
        raise ValueError("Chromosomy muszą mieć taką samą długość.")
    point = random.randint(1, len(gene1) - 1)
    child_gene1 = gene1[:point] + gene2[point:]
    child_gene2 = gene2[:point] + gene1[point:]
    return Individual(Chromosome(child_gene1)), Individual(Chromosome(child_gene2))

def one_point_mutation(individual: Individual, mutation_probability: float):
    """
    Mutacja jednopunktowa: dla każdego genu z prawdopodobieństwem mutation_probability następuje zmiana.
    :param individual: osobnik, który ulega mutacji
    :param mutation_probability: prawdopodobieństwo mutacji pojedynczego genu
    :return: nowy osobnik po mutacji
    """
    gene = list(individual.chromosome.gene)
    for i in range(len(gene)):
        if random.random() < mutation_probability:
            gene[i] = '1' if gene[i] == '0' else '0'
    mutated_gene = ''.join(gene)
    return Individual(Chromosome(mutated_gene))

# Możesz dodać kolejne funkcje, np. two_point_crossover, uniform_crossover, two_point_mutation, operator inwersji itd.
