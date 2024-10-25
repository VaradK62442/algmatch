"""
Class to read in a file of preferences for the Stable Marriage Problem stable matching algorithm.
"""

from abstractClasses.abstractReader import AbstractReader


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_men = 0
        self.no_women = 0
        self.men = {}                
        self.women = {}
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        self.no_men, self.no_women = map(int, file[0].split())

        # build men dictionary
        for elt in file[1:self.no_men+1]:
            entry = elt.split()
            man = f"m{entry[0]}"
            preferences = [f"w{i}" for i in entry[1:]]

            rank = {woman: idx for idx, woman in enumerate(preferences)}
            self.men[man] = {"list": preferences, "rank": rank}

        # build women dictionary
        for elt in file[self.no_men+1:self.no_men+self.no_women+1]:
            entry = elt.split()
            woman = f"w{entry[0]}"
            preferences = [f"m{i}" for i in entry[1:]]

            rank = {man: idx for idx, man in enumerate(preferences)}
            self.women[woman] = {"list": preferences, "rank": rank}