import random
from backend.models.individual import Individual
from backend.models.chromosome import Chromosome
# Importujemy interfejsy operatorów z modułu operators
from backend.services.operators import SelectionOperator, CrossoverOperator, MutationOperator, InversionOperator

class Population:
    def __init__(self, population_size: int):
        """
        Inicjalizacja populacji osobników.
        :param population_size: liczba osobników w populacji
        """
        self.population_size = population_size
        self.individuals = []

    def initialize(self, chromosome_length: int) -> None:
        """
        Losowa inicjalizacja populacji. Każdy osobnik otrzymuje pojedynczy losowy chromosom o zadanej długości.
        :param chromosome_length: długość chromosomu
        """
        self.individuals = [
            Individual(Chromosome.random(chromosome_length))
            for _ in range(self.population_size)
        ]

    def evaluate(self, fitness_function) -> None:
        """
        Ocena funkcji celu (fitness) dla każdego osobnika w populacji.
        :param fitness_function: instancja klasy FitnessFunction z metodą evaluate(phenotype)
        """
        for individual in self.individuals:
            # Przyjmujemy stały zakres poszukiwań, np. [-65.536, 65.536]
            phenotype = individual.get_phenotype(-65.536, 65.536)
            individual.fitness = fitness_function.evaluate(phenotype)

    def get_best(self, n: int):
        """
        Zwraca n najlepszych osobników (przyjmując, że niższa wartość fitness oznacza lepsze rozwiązanie).
        :param n: liczba najlepszych osobników do zwrócenia
        :return: lista n najlepszych osobników
        """
        sorted_individuals = sorted(self.individuals, key=lambda ind: ind.fitness)
        return sorted_individuals[:n]

    def evolve(self, fitness_function,
           selection_operator: SelectionOperator,
           crossover_operator: CrossoverOperator,
           mutation_operator: MutationOperator,
           inversion_operator: InversionOperator, 
           crossover_probability: float,
           mutation_probability: float,
           inversion_probability: float,
           elitism_count: int,
           **selection_params):
        # Ocena populacji
        self.evaluate(fitness_function)
        
        # Wybór rodziców przy użyciu operatora selekcji
        parents = selection_operator.select(self, **selection_params)
        
        offspring = []
        # Generowanie potomstwa z uwzględnieniem prawdopodobieństwa krzyżowania
        while len(offspring) < self.population_size - elitism_count:
            parent1, parent2 = random.sample(parents, 2)
            if random.random() < crossover_probability:
                child1, child2 = crossover_operator.crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            offspring.extend([child1, child2])
        offspring = offspring[:self.population_size - elitism_count]
        
        # Mutacja potomstwa
        mutated_offspring = [mutation_operator.mutate(child, mutation_probability) for child in offspring]
        
        # Inwersja potomstwa
        inverted_offspring = [inversion_operator.invert(child, inversion_probability) for child in mutated_offspring]
        
        # Zachowanie elitarnych osobników (najlepszych)
        elite = self.get_best(elitism_count)
        
        # Aktualizacja populacji
        self.individuals = elite + inverted_offspring
        
        # Opcjonalnie: ponowna ocena populacji
        self.evaluate(fitness_function)