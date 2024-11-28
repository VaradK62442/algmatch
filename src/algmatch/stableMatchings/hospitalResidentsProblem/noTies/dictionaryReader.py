"""
Class to read in a dictionary of preferences for the Hospital/Residents Problem stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import CapacityError, IDMisformatError, RepeatIDError, PrefListMisformatError


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
                            raise IDMisformatError("resident",k)
                        resident = f"r{k}"
                        if resident in self.residents:
                            raise RepeatIDError("resident",k)
                        
                        for i in v:
                            if type(i) is not int:
                                raise PrefListMisformatError("resident",k,i)
                        preferences = [f"h{i}" for i in v]

                        self.residents[resident] = {"list": preferences, "rank": {}}

                case "hospitals":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise IDMisformatError("hospital", k)
                        hospital = f"h{k}"
                        if hospital in self.hospitals:
                            raise RepeatIDError("hospital", k)
                        
                        if type(v["capacity"]) is not int:
                            raise CapacityError("hospital",k)
                        capacity = v["capacity"]
                        
                        for i in v["preferences"]:
                            if type(i) is not int:
                                raise PrefListMisformatError("hospital",k,i,line=True)
                        preferences = [f"r{i}" for i in v["preferences"]]

                        self.hospitals[hospital] = {"capacity": capacity, "list": preferences, "rank": {}}