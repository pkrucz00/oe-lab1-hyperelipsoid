from collections.abc import Iterable

class HyperellipsoidFitness:
    def __init__(self, num_vars, search_range):
        self.num_vars = num_vars
        self.search_range = search_range

    def evaluate(self, phenotype):
        # Przyjmujemy, że phenotype to pojedyncza wartość – w praktyce możesz rozszerzyć na wielowymiarowość
        # Poniższa implementacja jest przykładowa
        value = 0
        # Jeśli phenotype jest pojedynczą wartością, używamy jej kwadratu
        # Dla wielowymiarowego problemu phenotype może być listą wartości
        if isinstance(phenotype, Iterable):
            for i in range(len(phenotype)):
                for j in range(i+1):
                    value += phenotype[j] ** 2
        else:
            value = phenotype ** 2
        return value
