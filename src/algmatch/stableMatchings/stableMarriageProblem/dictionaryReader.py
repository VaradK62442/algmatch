"""
Class to read in a dictionary of preferences for the Student Project Allocation stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.abstractClasses.abstractReader import ReaderError

class DictionaryReader(AbstractReader):
    def __init__(self, dictionary: dict) -> None:
        super().__init__(dictionary)
        self._read_data()

    def _read_data(self) -> None:
        self.men = {}
        self.women = {}

        for key, value in self.data.items():
            match key:
                case "men":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise ReaderError(f"man {k}", "Man ID misformatted")
                        man = f"m{k}"
                        if man in self.men:
                            raise ReaderError(f"man {k}", "Repeated man ID")
                        preferences = [f"w{i}" for i in v]

                        self.men[man] = {"list": preferences, "rank": {}}

                case "women":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise ReaderError(f"woman {k}", "Woman ID misformatted")
                        woman = f"w{k}"
                        if woman in self.women:
                            raise ReaderError(f"woman {k}", "Repeated woman ID")
                        preferences = [f"m{i}" for i in v]

                        self.women[woman] = {"list": preferences, "rank": {}}