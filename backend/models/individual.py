from backend.models.chromosome import Chromosome

class Individual:
    def __init__(self, chromosome_x: Chromosome, chromosome_y: Chromosome):
        """
        Inicjalizacja osobnika z pojedynczym chromosomem.
        :param chromosome: instancja Chromosome
        """
        self.chromosome_x = chromosome_x
        self.chromoseme_y = chromosome_y
        self.fitness = None  # wartość funkcji celu, ustalana później

    def get_phenotype(self, a: float, b: float) -> float:
        """
        Zwraca zdekodowaną wartość (fenotyp) chromosomu.
        :param a: dolny zakres poszukiwań
        :param b: górny zakres poszukiwań
        :return: wartość dziesiętna
        """
        return (self.chromosome_x.decode(a, b), self.chromoseme_y.decode(a, b))

    def __str__(self):
        phenotype = self.get_phenotype(-65.536, 65.536)
        return f"Individual(phenotype={phenotype}, fitness={self.fitness})"

