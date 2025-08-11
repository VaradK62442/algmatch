"""
Class to read in a dictionary of preferences for the Hospital/Residents Problem stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
    CapacityError,
    IDMisformatError,
    PrefListMisformatError,
    RepeatIDError,
)


class DictionaryReader(AbstractReader):
    def __init__(self, dictionary: dict) -> None:
        super().__init__(dictionary)
        self._read_data()

    def _read_data(self) -> None:
        self.residents = {}
        self.hospitals = {}

        for key, value in self.data.items():
            match key:
                case "residents":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise IDMisformatError("resident", k)
                        resident = f"r{k}"
                        if resident in self.residents:
                            raise RepeatIDError("resident", k)

                        for i in v:
                            # if not int, must be a tie list
                            if type(i) is not int and not all(
                                type(j) is int for j in i
                            ):
                                raise PrefListMisformatError("resident", k, i)
                        preferences = []
                        for i, elt in enumerate(v):
                            if isinstance(elt, int):
                                tie = set()
                                tie.add(f"h{elt}")
                            else:
                                tie = {f"h{j}" for j in elt}
                            preferences.append(tie)

                        self.residents[resident] = {"list": preferences, "rank": {}}

                case "hospitals":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise IDMisformatError("hospital", k)
                        hospital = f"h{k}"
                        if hospital in self.hospitals:
                            raise RepeatIDError("hospital", k)

                        if type(v["capacity"]) is not int:
                            raise CapacityError("hospital", k)
                        capacity = v["capacity"]

                        for i in v["preferences"]:
                            # if not int, must be a tie list
                            if type(i) is not int and not all(
                                type(j) is int for j in i
                            ):
                                raise PrefListMisformatError("hospital", k, i)
                        preferences = []
                        for i, elt in enumerate(v["preferences"]):
                            if isinstance(elt, int):
                                tie = set()
                                tie.add(f"r{elt}")
                            else:
                                tie = {f"r{j}" for j in elt}
                            preferences.append(tie)

                        self.hospitals[hospital] = {
                            "capacity": capacity,
                            "list": preferences,
                            "rank": {},
                        }
