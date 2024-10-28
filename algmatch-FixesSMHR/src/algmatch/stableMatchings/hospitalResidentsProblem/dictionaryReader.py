"""
Class to read in a dictionary of preferences for the Hospital/Residents Problem stable matching algorithm.
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

                        self.residents[resident] = {"list": preferences, "rank": {}}

                case "hospitals":
                    for k, v in value.items():
                        hospital = f"h{k}"
                        capacity = v["capacity"]
                        preferences = [f"r{i}" for i in v["preferences"]]

                        self.hospitals[hospital] = {"capacity": capacity, "list": preferences, "rank": {}}

        #remove unacceptable pairs
        for r, r_prefs in self.residents.items():
            acceptable_r_prefs = []
            for h in r_prefs["list"]:
                if r in self.hospitals[h]["list"]:
                    acceptable_r_prefs.append(h)
            self.residents[r]["list"] = acceptable_r_prefs
            self.residents[r]["rank"] = {hospital: idx for idx, hospital in enumerate(acceptable_r_prefs)}
            
        for h, h_prefs in self.hospitals.items():
            acceptable_h_prefs = []
            for r in h_prefs["list"]:
                if h in self.residents[r]["list"]:
                    acceptable_h_prefs.append(r)
            self.hospitals[h]["list"] = acceptable_h_prefs
            self.hospitals[h]["rank"] = {resident: idx for idx, resident in enumerate(acceptable_h_prefs)}