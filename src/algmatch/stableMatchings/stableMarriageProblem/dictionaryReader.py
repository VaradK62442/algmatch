"""
Class to read in a dictionary of preferences for the Student Project Allocation stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import IDMisformatError, RepeatIDError, PrefListMisformatError

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
                            raise IDMisformatError("man", k)
                        man = f"m{k}"
                        if man in self.men:
                            raise RepeatIDError("man", k)
                        
                        for i in v:
                            if type(i) is not int:
                                raise PrefListMisformatError("man", k, i)
                        preferences = [f"w{i}" for i in v]

                        self.men[man] = {"list": preferences, "rank": {}}

                case "women":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise IDMisformatError("woman", k)
                        woman = f"w{k}"
                        if woman in self.women:
                            raise RepeatIDError("woman", k)
                        
                        for i in v:
                            if type(i) is not int:
                                 raise PrefListMisformatError("woman", k, i)
                        preferences = [f"m{i}" for i in v]

                        self.women[woman] = {"list": preferences, "rank": {}}