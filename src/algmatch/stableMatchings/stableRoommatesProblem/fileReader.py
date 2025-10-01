"""
Class to read in a file of preferences for the Stable Roommates Problem stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
    IDMisformatError,
    RepeatIDError,
    PrefListMisformatError,
)


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_roommates = 0
        self.roommates = {}
        cur_line = 1

        with open(self.data, "r") as file:
            file = file.read().splitlines()

        for elt in file[:self.no_roommates]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("roommate", cur_line, line=True)
            roommate = f"r{entry[0]}"
            if roommate in self.roommates:
                raise RepeatIDError("roommate", cur_line, line=True)

            for i in entry[1:]:
                if not i.isdigit() or entry[0] == i: # self-ranking is illegal
                    raise PrefListMisformatError("roommate", cur_line, i, line=True)
            preferences = [f"r{i}" for i in entry[1:]]

            self.roommates[roommate] = {"list": preferences, "rank": {}}