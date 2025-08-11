"""
Class to read in a file of preferences for the Stable Marriage Problem stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
    IDMisformatError,
    RepeatIDError,
    PrefListMisformatError,
)


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
                            # if not int, must be a tie list
                            if type(i) is not int and not all(
                                type(j) is int for j in i
                            ):
                                raise PrefListMisformatError("man", k, i)
                        preferences = []
                        for i, elt in enumerate(v):
                            if isinstance(elt, int):
                                tie = set()
                                tie.add(f"w{elt}")
                            else:
                                tie = {f"w{j}" for j in elt}
                            preferences.append(tie)

                        self.men[man] = {"list": preferences, "rank": {}}

                case "women":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise IDMisformatError("woman", k)
                        woman = f"w{k}"
                        if woman in self.women:
                            raise RepeatIDError("woman", k)

                        for i in v:
                            # if not int, must be a tie list
                            if type(i) is not int and not all(
                                type(j) is int for j in i
                            ):
                                raise PrefListMisformatError("woman", k, i)
                        preferences = []
                        for i, elt in enumerate(v):
                            if isinstance(elt, int):
                                tie = set()
                                tie.add(f"m{elt}")
                            else:
                                tie = {f"m{j}" for j in elt}
                            preferences.append(tie)

                        self.women[woman] = {"list": preferences, "rank": {}}
