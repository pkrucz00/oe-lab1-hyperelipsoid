from backend.models.chromosome import Chromosome

class Individual:
    def __init__(self, chromosome: Chromosome):
        """
        Inicjalizacja osobnika z pojedynczym chromosomem.
        :param chromosome: instancja Chromosome
        """
        self.chromosome = chromosome
        self.fitness = None  # wartość funkcji celu, ustalana później

    def get_phenotype(self, a: float, b: float) -> float:
        """
        Zwraca zdekodowaną wartość (fenotyp) chromosomu.
        :param a: dolny zakres poszukiwań
        :param b: górny zakres poszukiwań
        :return: wartość dziesiętna
        """
        return self.chromosome.decode(a, b)

    def __str__(self):
        phenotype = self.get_phenotype(-65.536, 65.536)
        return f"Individual(phenotype={phenotype}, fitness={self.fitness})"

