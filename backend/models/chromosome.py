import random
import math

class Chromosome:
    def __init__(self, gene: str):
        """
        Inicjalizacja chromosomu zadaną reprezentacją binarną.
        :param gene: ciąg znaków '0' i '1'
        """
        self.gene = gene

    @staticmethod
    def random(length: int) -> "Chromosome":
        """
        Generuje losowy chromosom o podanej długości.
        :param length: długość chromosomu
        :return: instancja Chromosome
        """
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