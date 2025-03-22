# from domain.problem_function import hyperelipsoid

# print(hyperelipsoid([1, 2, 3]))


from backend.models.chromosome import Chromosome
from backend.models.indyvidual import Individual


# Przykładowe użycie:
if __name__ == "__main__":
    # Generowanie losowego chromosomu o długości 10
    chrom = Chromosome.random(10)
    print("Losowy chromosom:", chrom)
    
    # Dekodowanie chromosomu w przedziale [-65.536, 65.536]
    decoded_value = chrom.decode(-65.536, 65.536)
    print("Zdekodowana wartość:", decoded_value)

    # Tworzenie osobnika z pojedynczym losowym chromosomem
    individual = Individual(Chromosome.random(10))
    print("Osobnik:", individual)