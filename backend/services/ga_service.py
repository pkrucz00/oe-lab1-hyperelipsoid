import time
import math
from backend.models.population import Population
from backend.services.operators import *
from typing import Literal
from backend.models.fitness import HyperellipsoidFitness


def calculate_chromosome_length(search_range, precision):
    a, b = search_range
    # Obliczamy minimalną liczbę bitów m tak, aby pokryć zakres z daną precyzją
    m = math.ceil(math.log2((b - a) * (10 ** precision) + 1))
    return m

def choose_selection_method(selection_method, tournament_size, best_count):
    if selection_method.lower() == "tournament":
        return TournamentSelection(tournament_size=tournament_size)
    elif selection_method.lower() == "roulette":
        return RouletteSelection()
    elif selection_method.lower() == "best":
        return BestSelection(count=best_count)
    else:
        # Domyślnie Tournament
        return TournamentSelection(tournament_size=tournament_size)

def choose_crossover_method(crossover_method):
    if crossover_method.lower() == "one_point":
        return OnePointCrossover()
    elif crossover_method.lower() == "two_point":
        return  TwoPointCrossover()
    elif crossover_method.lower() == "uniform":
        return  UniformCrossover()
    elif crossover_method.lower() == "grain":
        return GrainCrossover()
    else:
        return OnePointCrossover()

def choose_mutation_method(mutation_method):
    if mutation_method.lower() == "one_point":
        return OnePointMutation()
    elif mutation_method.lower() == "boundary":
        return BoundaryMutation()
    elif mutation_method.lower() == "two_point":
        return TwoPointMutation()
    else:
        return OnePointMutation()
    

def run_ga(representation: Literal['binary', 'real'], config: dict) -> dict:
    start_time = time.time()

    # Odczyt parametrów z JSON
    pop_size = config.get("population_size", 100)
    epochs = config.get("epochs", 50)
    search_range = config.get("search_range", [-65.536, 65.536])
    precision = config.get("precision", 6)
    
    # Parametry operatorów
    tournament_size = config.get("tournament_size", 3)
    crossover_probability = config.get("crossover_probability", 0.8)
    mutation_probability = config.get("mutation_probability", 0.3)
    inversion_probability = 0. if representation == 'real' else config.get("inversion_probability", 0.3)
    elitism_count = config.get("elitism_count", 2)
    
    # Wyliczamy długość chromosomu dla jednej zmiennej
    chromosome_length = calculate_chromosome_length(search_range, precision)
    
    fitness_function = HyperellipsoidFitness()
    
    # Inicjalizacja populacji
    ## TODO add chromosome type
    population = Population(pop_size, chromosome_length)
    
    # Odczyt dodatkowych parametrów dotyczących metod operatorów
    selection_method = config.get("selection_method", "tournament")
    crossover_method = config.get("crossover_method", "one_point")
    mutation_method = config.get("mutation_method", "one_point")
    
    selection_operator = choose_selection_method(selection_method, tournament_size, config.get("best_count", 3))
    crossover_operator = choose_crossover_method(crossover_method=crossover_method)
    mutation_operator = choose_mutation_method(mutation_method)
    inversion_operator = SimpleInversion() 

    history = []
    for _epoch in range(epochs):
        population.evolve(
            fitness_function,
            selection_operator=selection_operator,
            crossover_operator=crossover_operator,
            mutation_operator=mutation_operator,
            inversion_operator=inversion_operator,
            crossover_probability=crossover_probability,
            mutation_probability=mutation_probability,
            inversion_probability=inversion_probability,
            elitism_count=elitism_count
        )
        best_individual = population.get_best(1)[0]
        (best_x, best_y) = best_individual.get_phenotype(search_range[0], search_range[1])
        best_fitness = best_individual.fitness
        history.append({"x": best_x, "y": best_y, "fitness": best_fitness})

    elapsed_time = time.time() - start_time
    best_individual = population.get_best(1)[0]

    result = {
        "best_fitness": best_individual.fitness,
        "best_individual": best_individual.get_phenotype(search_range[0], search_range[1]),
        "history": history,
        "time": elapsed_time
    }
    
    return result
