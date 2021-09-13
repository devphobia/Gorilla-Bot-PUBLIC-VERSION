# imports

from random import randint

class Shuffler:
    def __init__(self):
        self.__elements = []

    @property
    def elements(self):
        return self.__elements
    
    # Adiciona um elemento à caixinha de sorteio
    # Adds an element to the shuffle box
    
    def add_element(self, element):
        self.elements.append(element)

    # Pega um elemento aleatório da caixinha de sorteio
    # Gets a random element from the shuffle box
    
    def random_element(self):
        return self.elements[randint(0, len(self.elements))]

    # Deixa a caixinha de sorteio vazia
    # Resets the shuffle box
    
    def clear(self):
        self.__elements = []
