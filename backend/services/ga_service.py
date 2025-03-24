import time
import math
import random
from backend.models.population import Population
from backend.services.operators import *

def calculate_chromosome_length(search_range, precision):
    a, b = search_range
    # Obliczamy minimalną liczbę bitów m tak, aby pokryć zakres z daną precyzją
    m = math.ceil(math.log2((b - a) * (10 ** precision) + 1))
    return m

def run_ga(config: dict) -> dict:
    start_time = time.time()
    
    # Odczyt parametrów z JSON
    function_name = config.get("function", "hyperellipsoid")
    num_vars = config.get("variables", 10)
    pop_size = config.get("population_size", 100)
    epochs = config.get("epochs", 50)
    search_range = config.get("search_range", [-65.536, 65.536])
    precision = config.get("precision", 6)
    optimization_type = config.get("optimization_type", "minimization")
    
    # Parametry operatorów
    tournament_size = config.get("tournament_size", 3)
    crossover_probability = config.get("crossover_probability", 0.8)
    mutation_probability = config.get("mutation_probability", 0.3)
    inversion_probability = config.get("inversion_probability", 0.3)
    elitism_count = config.get("elitism_count", 2)
    
    # Wyliczamy długość chromosomu dla jednej zmiennej
    chromosome_length = calculate_chromosome_length(search_range, precision)
    
    # Inicjalizacja funkcji celu – przykładowo Hyperellipsoid
    if function_name.lower() == "hyperellipsoid":
        from backend.models.fitness import HyperellipsoidFitness
        fitness_function = HyperellipsoidFitness(num_vars=num_vars, search_range=search_range)
    else:
        # Domyślnie Hyperellipsoid
        from backend.models.fitness import HyperellipsoidFitness
        fitness_function = HyperellipsoidFitness(num_vars=num_vars, search_range=search_range)
    
    # Inicjalizacja populacji
    population = Population(pop_size)
    population.initialize(chromosome_length)
    
    # Odczyt dodatkowych parametrów dotyczących metod operatorów
    selection_method = config.get("selection_method", "tournament")
    crossover_method = config.get("crossover_method", "one_point")
    mutation_method = config.get("mutation_method", "one_point")
    inversion_method = config.get("inversion_method", "simple")
    
    # Inicjalizacja operatora selekcji
    if selection_method.lower() == "tournament":
        
        selection_operator = TournamentSelection(tournament_size=tournament_size)
    elif selection_method.lower() == "roulette":

        selection_operator = RouletteSelection()
    elif selection_method.lower() == "best":

        best_count = config.get("best_count", 3)
        selection_operator = BestSelection(count=best_count)
    else:
        # Domyślnie Tournament

        selection_operator = TournamentSelection(tournament_size=tournament_size)
    
    # Inicjalizacja operatora krzyżowania
    if crossover_method.lower() == "one_point":

        crossover_operator = OnePointCrossover()
    elif crossover_method.lower() == "two_point":

        crossover_operator = TwoPointCrossover()
    elif crossover_method.lower() == "uniform":

        crossover_operator = UniformCrossover()
    elif crossover_method.lower() == "grain":

        crossover_operator = GrainCrossover()
    else:

        crossover_operator = OnePointCrossover()
    
    # Inicjalizacja operatora mutacji
    if mutation_method.lower() == "one_point":

        mutation_operator = OnePointMutation()
    elif mutation_method.lower() == "boundary":

        mutation_operator = BoundaryMutation()
    elif mutation_method.lower() == "two_point":

        mutation_operator = TwoPointMutation()
    else:

        mutation_operator = OnePointMutation()
    
    # Inicjalizacja operatora inwersji
    if inversion_method.lower() == "simple":

        inversion_operator = SimpleInversion()
    else:

        inversion_operator = SimpleInversion()


    history = []
    for epoch in range(epochs):
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
        best_x = best_individual.get_phenotype(search_range[0], search_range[1])
        best_fitness = best_individual.fitness
        history.append({"x": best_x, "fitness": best_fitness})

    elapsed_time = time.time() - start_time
    best_individual = population.get_best(1)[0]

    result = {
        "best_fitness": best_individual.fitness,
        "best_individual": best_individual.get_phenotype(search_range[0], search_range[1]),
        "history": history,
        "time": elapsed_time
    }
    
    return result
