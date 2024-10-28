"""
Class to read in a file of preferences for the Hospitals/Residents Problem stable matching algorithm.
"""

from abstractClasses.abstractReader import AbstractReader

class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_residents = 0
        self.no_hospitals = 0
        self.residents = {}                
        self.hospitals = {}
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        self.no_residents, self.no_hospitals = map(int, file[0].split())

        # build residents dictionary
        for elt in file[1:self.no_residents+1]:
            entry = elt.split()
            resident = f"r{entry[0]}"
            preferences = [f"h{i}" for i in entry[1:]]

            self.residents[resident] = {"list": preferences, "rank": {}}

        # build hospitals dictionary
        for elt in file[self.no_residents+1:self.no_residents+self.no_hospitals+1]:
            entry = elt.split()
            hospital = f"h{entry[0]}"
            capacity = int(entry[1])
            preferences = [f"r{i}" for i in entry[2:]]

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

