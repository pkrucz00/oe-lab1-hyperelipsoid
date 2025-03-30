import random
from abc import ABC, abstractmethod
from backend.models.individual import Individual
from backend.models.chromosome import Chromosome

# --- SELEKCJA ---

class SelectionOperator(ABC):
    @abstractmethod
    def select(self, population, **kwargs):
        """
        Wybiera osobniki z populacji.
        """
        pass

class TournamentSelection(SelectionOperator):
    def __init__(self, tournament_size=3):
        self.tournament_size = tournament_size

    def select(self, population, **kwargs):
        selected = []
        pop = population.individuals
        for _ in range(len(pop)):
            tournament = random.sample(pop, self.tournament_size)
            best = min(tournament, key=lambda ind: ind.fitness)  # Zakładamy minimalizację
            selected.append(best)
        return selected

class RouletteSelection(SelectionOperator):
    def select(self, population, **kwargs):
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

class BestSelection(SelectionOperator):
    def __init__(self, count):
        self.count = count

    def select(self, population, **kwargs):
        sorted_individuals = sorted(population.individuals, key=lambda ind: ind.fitness)
        return sorted_individuals[:self.count]

# --- KRZYŻOWANIE ---

class CrossoverOperator(ABC):

    def crossover(self, parent1: Individual, parent2: Individual):
        """
        Krzyżuje dwóch rodziców i zwraca parę potomków.
        """
        (x_gene_1, y_gene_1), (x_gene_2, y_gene_2) = parent1.get_genes(), parent2.get_genes()
        (new_gene_x_1, new_gene_y_1), (new_gene_x_2, new_gene_y_2) = self.gene_crossover(x_gene_1, x_gene_2), self.gene_crossover(y_gene_1, y_gene_2)
        
        individual1 = Individual(Chromosome(new_gene_x_1), Chromosome(new_gene_y_1))
        individual2 = Individual(Chromosome(new_gene_x_2), Chromosome(new_gene_y_2))
        return individual1, individual2
        
    @abstractmethod
    def gene_crossover(self, gene1: str, gene2: str) -> tuple[str, str]:
        '''
        Krzyżuje dwa geny i zwraca parę genów potomnych
        '''
        pass

class OnePointCrossover(CrossoverOperator):
    def gene_crossover(self, gene1: str, gene2: str) -> tuple[str, str]:
        if len(gene1) != len(gene2):
            raise ValueError("Chromosomy muszą mieć taką samą długość.")
        point = random.randint(1, len(gene1) - 1)
        child_gene1 = gene1[:point] + gene2[point:]
        child_gene2 = gene2[:point] + gene1[point:]
        return child_gene1, child_gene2

class TwoPointCrossover(CrossoverOperator):
    def gene_crossover(self, gene1: str, gene2: str) -> tuple[str, str]:
        if len(gene1) != len(gene2):
            raise ValueError("Chromosomy muszą mieć taką samą długość.")
        if len(gene1) < 2:
            return OnePointCrossover().crossover(gene1, gene2)
        
        point1, point2 = sorted(random.sample(range(1, len(gene1)), 2))
        child_gene1 = gene1[:point1] + gene2[point1:point2] + gene1[point2:]
        child_gene2 = gene2[:point1] + gene1[point1:point2] + gene2[point2:]
        return child_gene1, child_gene2

class UniformCrossover(CrossoverOperator):
    def gene_crossover(self, gene1: str, gene2: str) -> tuple[str, str]:
        if len(gene1) != len(gene2):
            raise ValueError("Chromosomy muszą mieć taką samą długość.")
        child_gene1 = ''.join(g1 if random.random() < 0.5 else g2 for g1, g2 in zip(gene1, gene2))
        child_gene2 = ''.join(g2 if random.random() < 0.5 else g1 for g1, g2 in zip(gene1, gene2))
        return child_gene1, child_gene2

class GrainCrossover(CrossoverOperator):
    def gene_crossover(self, gene1: str, gene2: str):
        if len(gene1) != len(gene2):
            raise ValueError("Chromosomy muszą mieć taką samą długość.")
        
        child_gene1 = ""
        child_gene2 = ""
        for i in range(len(gene1)):
            # Dla potomka 1 losujemy osobno dla każdego genu
            if random.random() <= 0.5:
                child_gene1 += gene1[i]
            else:
                child_gene1 += gene2[i]
            # Dla potomka 2 również losujemy niezależnie
            if random.random() <= 0.5:
                child_gene2 += gene1[i]
            else:
                child_gene2 += gene2[i]
                
        return child_gene1, child_gene2


# --- MUTACJA ---

class MutationOperator(ABC):
    def mutate(self, individual: Individual, mutation_probability: float):
        """
        Mutuje danego osobnika z podanym prawdopodobieństwem.
        """
        if random.random() > mutation_probability:
            return individual
        
        x_gene, y_gene = individual.get_genes()
        new_gene_x, new_gene_y = self.mutate_gene(x_gene), self.mutate_gene(y_gene)
        
        return Individual(Chromosome(new_gene_x), Chromosome(new_gene_y))
    
    @abstractmethod
    def mutate_gene(self, gene: str) -> str:
        pass

class OnePointMutation(MutationOperator):
    def mutate_gene(self, gene: str)-> str:
        # Losujemy, czy mutacja ma zajść – jeśli nie, zwracamy osobnika bez zmian
        
        gene = list(gene)
        # Wybieramy losowy indeks w chromosomie
        index = random.randint(0, len(gene) - 1)
        gene[index] = '1' if gene[index] == '0' else '0'
        return ''.join(gene)


class BoundaryMutation(MutationOperator):
    def mutate_gene(self, gene: str) -> str:
        gene = list(gene)
        # Losowo wybieramy, czy zmodyfikować pierwszy czy ostatni bit
        if random.random() < 0.5:
            # Mutacja pierwszego bitu
            gene[0] = '1' if gene[0] == '0' else '0'
        else:
            # Mutacja ostatniego bitu
            gene[-1] = '1' if gene[-1] == '0' else '0'
        return ''.join(gene)

class TwoPointMutation(MutationOperator):
    def mutate_gene(self, gene: str) -> str:
        gene = list(gene)
        if len(gene) < 2:
            return gene
        i, j = random.sample(range(len(gene)), 2)
        gene[i] = '1' if gene[i] == '0' else '0'
        gene[j] = '1' if gene[j] == '0' else '0'
        return ''.join(gene)


# --- INWERSJA ---

class InversionOperator(ABC):
    def invert(self, individual: Individual, inversion_probability: float) -> Individual:
        """
        Stosuje inwersję na chromosomie osobnika z zadanym prawdopodobieństwem.
        """
        if random.random() > inversion_probability:
            return individual
        
        x_gene, y_gene = individual.get_genes()
        new_gene_x, new_gene_y = self.invert_gene(x_gene), self.invert_gene(y_gene)
        
        return Individual(Chromosome(new_gene_x), Chromosome(new_gene_y))
        
    @abstractmethod
    def invert_gene(self, gene: str) -> str:
        pass

class SimpleInversion(InversionOperator):
    def invert_gene(self, gene: str) -> str:
        gene = list(gene)
            # Wybieramy dwa losowe indeksy i odwracamy fragment między nimi
        i, j = sorted(random.sample(range(len(gene)), 2))
        gene[i:j+1] = reversed(gene[i:j+1])
        return ''.join(gene)
