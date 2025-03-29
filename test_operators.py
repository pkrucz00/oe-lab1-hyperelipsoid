import random
from backend.models.chromosome import Chromosome
from backend.models.individual import Individual
from backend.services.operators import *

# Prosta funkcja fitness do testów – tutaj po prostu zwracamy wartość fenotypu
def dummy_fitness(phenotype):
    return phenotype

def print_individual(ind, label=""):
    # Dla testu używamy zakresu dekodowania [-65.536, 65.536]
    phenotype = ind.get_phenotype(-65.536, 65.536)
    print(f"{label} Chromosome: {ind.chromosome.gene} | Phenotype: {phenotype:.4f} | Fitness: {ind.fitness}")

def test_selection():
    print("----- Test operatorów selekcji -----")
    # Tworzymy przykładową populację – minimalna klasa kontenera
    individuals = [
        Individual(Chromosome("101010"), Chromosome("101010")),
        Individual(Chromosome("010101"), Chromosome("010101")),
        Individual(Chromosome("111000"), Chromosome("111000")),
        Individual(Chromosome("000111"), Chromosome("000111")),
        Individual(Chromosome("110011"), Chromosome("110011")),
        Individual(Chromosome("111111"), Chromosome("111111"))
    ]
    # Ustawiamy fitness – korzystamy z dekodowania jako wartości fitness
    for ind in individuals:
        ph = ind.get_phenotype(-65.536, 65.536)
        ind.fitness = dummy_fitness(ph)
    
    class DummyPopulation:
        def __init__(self, individuals):
            self.individuals = individuals

    pop = DummyPopulation(individuals)
    
    # Test turniejowej selekcji
    tournament = TournamentSelection(tournament_size=2)
    selected_tournament = tournament.select(pop)
    print("\nTournament Selection:")
    for ind in selected_tournament:
        print_individual(ind)
    
    # Test ruletkowej selekcji
    roulette = RouletteSelection()
    selected_roulette = roulette.select(pop)
    print("\nRoulette Selection:")
    for ind in selected_roulette:
        print_individual(ind)
    
    # Test selekcji najlepszych – wybieramy 2 najlepsze
    best = BestSelection(count=2)
    selected_best = best.select(pop)
    print("\nBest Selection:")
    for ind in selected_best:
        print_individual(ind)

def test_crossover():
    print("\n----- Test operatorów krzyżowania -----")
    # Tworzymy dwóch przykładowych rodziców
    parent1 = Individual(Chromosome("1010101010"))
    parent2 = Individual(Chromosome("0101010101"))
    print("Rodzic 1:")
    print_individual(parent1)
    print("Rodzic 2:")
    print_individual(parent2)
    
    # One-Point Crossover
    one_point = OnePointCrossover()
    child1, child2 = one_point.crossover(parent1, parent2)
    print("\nOne-Point Crossover:")
    print_individual(child1, "Potomek 1:")
    print_individual(child2, "Potomek 2:")
    
    # Two-Point Crossover
    two_point = TwoPointCrossover()
    child1, child2 = two_point.crossover(parent1, parent2)
    print("\nTwo-Point Crossover:")
    print_individual(child1, "Potomek 1:")
    print_individual(child2, "Potomek 2:")
    
    # Uniform Crossover
    uniform = UniformCrossover()
    child1, child2 = uniform.crossover(parent1, parent2)
    print("\nUniform Crossover:")
    print_individual(child1, "Potomek 1:")
    print_individual(child2, "Potomek 2:")
    
    # Grain (ziarniste) Crossover
    grain = GrainCrossover()
    child1, child2 = grain.crossover(parent1, parent2)
    print("\nGrain Crossover:")
    print_individual(child1, "Potomek 1:")
    print_individual(child2, "Potomek 2:")

def test_mutation():
    print("\n----- Test operatorów mutacji -----")
    original = Individual(Chromosome("1010101010"))
    print("Osobnik oryginalny:")
    print_individual(original)
    
    # One-Point Mutation (prawdopodobieństwo 0.5)
    one_point_mut = OnePointMutation()
    mutated = one_point_mut.mutate(original, 0.5)
    print("\nOne-Point Mutation (p=0.5):")
    print_individual(mutated)
    
    # Boundary Mutation (wymuszamy mutację, p=1.0)
    boundary_mut = BoundaryMutation()
    mutated = boundary_mut.mutate(original, 1.0)
    print("\nBoundary Mutation (p=1.0):")
    print_individual(mutated)
    
    # Two-Point Mutation (wymuszamy mutację, p=1.0)
    two_point_mut = TwoPointMutation()
    mutated = two_point_mut.mutate(original, 1.0)
    print("\nTwo-Point Mutation (p=1.0):")
    print_individual(mutated)

def test_inversion():
    print("\n----- Test operatora inwersji -----")
    original = Individual(Chromosome("1010101010"))
    print("Osobnik oryginalny:")
    print_individual(original)
    
    inversion = SimpleInversion()
    inverted = inversion.invert(original, 1.0)  # wymuszenie inwersji (p=1.0)
    print("\nSimple Inversion (p=1.0):")
    print_individual(inverted)

if __name__ == "__main__":
    test_selection()
    test_crossover()
    test_mutation()
    test_inversion()
