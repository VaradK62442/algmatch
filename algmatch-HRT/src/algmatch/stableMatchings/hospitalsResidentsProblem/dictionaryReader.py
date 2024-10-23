"""
Class to read in a dictionary of preferences for the Student Project Allocation stable matching algorithm.
"""

from abstractClasses.abstractReader import AbstractReader


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
                        resident = f"r{k}"
                        preferences = [f"h{i}" for i in v]
                        rank = {hospital: idx for idx, hospital in enumerate(preferences)}

                        self.residents[resident] = {"list": preferences, "rank": rank}

                case "hospitals":
                    for k, v in value.items():
                        hospital = f"h{k}"
                        capacity = v["capacity"]
                        preferences = [f"r{i}" for i in v["preferences"]]
                        rank = {resident: idx for idx, resident in enumerate(preferences)}

                        self.hospitals[hospital] = {"capacity": capacity, "list": preferences, "rank": rank}