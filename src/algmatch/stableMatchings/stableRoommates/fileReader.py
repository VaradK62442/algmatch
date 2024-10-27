"""
Class to read in a file of preferences for the Stable Roommates stable matching algorithm.
"""

from abstractClasses.abstractReader import AbstractReader


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.roommates = {}
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        for elt in file:
            entry = elt.split()
            roommate = f"r{entry[0]}"
            preferences = [f"r{i}" for i in entry[1:]]

            rank = {other: idx for idx, other in enumerate(preferences)}
            self.roommates[roommate] = {"list": preferences, "rank": rank}