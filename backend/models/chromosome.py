import random
import math

from abc import ABC, abstractmethod
from typing import Literal

def calculate_chromosome_length(search_range, precision):
    a, b = search_range
    # Obliczamy minimalną liczbę bitów m tak, aby pokryć zakres z daną precyzją
    m = math.ceil(math.log2((b - a) * (10 ** precision) + 1))
    return m

def get_chromosome_init(chromosome_type: Literal['binary', 'real'], search_range: tuple[float, float], precision: int):
    return lambda search_range: BinaryChromosome

class Chromosome(ABC):
    def __init__(self, search_range: tuple[float, float], precision: int):
        """
        Inicjalizacja chromosomu zadaną reprezentacją binarną.
        :param gene: ciąg znaków '0' i '1'
        """
        self.gene = gene

    @staticmethod
    def random(a: int, b: int) -> "Chromosome":
        """
        Generuje losowy chromosom o podanej długości.
        :param a: dolny zakres
        :param b: górny zakres
        :return: instancja Chromosome
        """
        length = calculate_chromosome_length((a, b))
        gene = ''.join(random.choice('01') for _ in range(length))
        return Chromosome(gene)

    def decode(self, a: float, b: float) -> float:
        """
        Dekoduje binarną reprezentację chromosomu na wartość dziesiętną.
        Wzór: x = a + decimal(gene) * (b - a) / (2^m - 1)
        gdzie m to długość łańcucha binarnego.
        
        :param a: dolny zakres poszukiwań
        :param b: górny zakres poszukiwań
        :return: wartość dziesiętna odpowiadająca reprezentacji binarnej
        """
        m = len(self.gene)
        # Konwersja łańcucha binarnego na wartość dziesiętną
        decimal_value = int(self.gene, 2)
        # Obliczenie x według wzoru
        x = a + decimal_value * (b - a) / (2**m - 1)
        return x

    def __str__(self):
        return f"Chromosome(gene='{self.gene}')"
    

def BinaryChromosome(Chromosome):
    pass

def RealChromosome(Chromosome):
    pass