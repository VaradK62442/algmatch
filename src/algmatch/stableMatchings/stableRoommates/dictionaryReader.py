"""
Class to read in a dictionary of preferences for the Stable Roommates stable matching algorithm.
"""

from abstractClasses.abstractReader import AbstractReader


class DictionaryReader(AbstractReader):
    def __init__(self, dictionary: dict) -> None:
        super().__init__(dictionary)
        self._read_data()

    def _read_data(self) -> None:
        self.roommates = {}

        for k, v in self.data.items():
            roommate = f"r{k}"
            preferences = [f"r{i}" for i in v]
            rank = {other: idx for idx, other in enumerate(preferences)}

            self.roommates[roommate] = {"list": preferences, "rank": rank}