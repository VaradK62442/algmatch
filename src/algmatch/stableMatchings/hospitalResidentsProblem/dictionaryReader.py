"""
Class to read in a dictionary of preferences for the Hospital/Residents Problem stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.abstractClasses.abstractReader import ReaderError

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
                            raise ReaderError(f"resident {k}", "Resident ID misformatted")
                        resident = f"r{k}"
                        if resident in self.residents:
                            raise ReaderError(f"resident {k}", "Repeated resident ID")
                        
                        for i in v:
                            if type(i) is not int:
                                raise ReaderError(f"resident {k}", "Resident preference list misformatted; {i} is not int")
                        preferences = [f"h{i}" for i in v]

                        self.residents[resident] = {"list": preferences, "rank": {}}

                case "hospitals":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise ReaderError(f"hospital {k}", "Hospital ID misformatted")
                        hospital = f"h{k}"
                        if hospital in self.hospitals:
                            raise ReaderError(f"hospital {k}", "Repeated hospital ID")
                        
                        if type(v["capacity"]) is not int:
                            raise ReaderError(f"hospital {k}", "Capacity is not int")
                        capacity = v["capacity"]
                        
                        for i in v:
                            if type(i) is not int:
                                raise ReaderError(f"hospital {k}", "Hospital preference list misformatted; {i} is not int")  
                        preferences = [f"r{i}" for i in v["preferences"]]

                        self.hospitals[hospital] = {"capacity": capacity, "list": preferences, "rank": {}}