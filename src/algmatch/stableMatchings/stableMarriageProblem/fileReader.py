"""
Class to read in a file of preferences for the Stable Marriage Problem stable matching algorithm.
"""

from abstractClasses.abstractReader import AbstractReader


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_men = 0
        self.no_women = 0
        self.men = {}                
        self.women = {}
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        self.no_men, self.no_women = map(int, file[0].split())

        # build men dictionary
        for elt in file[1:self.no_men+1]:
            entry = elt.split()
            man = f"m{entry[0]}"
            preferences = [f"w{i}" for i in entry[1:]]

            self.men[man] = {"list": preferences, "rank": {}}

        # build women dictionary
        for elt in file[self.no_men+1:self.no_men+self.no_women+1]:
            entry = elt.split()
            woman = f"w{entry[0]}"
            preferences = [f"m{i}" for i in entry[1:]]

            self.women[woman] = {"list": preferences, "rank": {}}

        #remove unacceptable pairs
        for m, m_prefs in self.men.items():
            acceptable_m_prefs = []
            for w in m_prefs["list"]:
                if m in self.women[w]["list"]:
                    acceptable_m_prefs.append(w)
            self.men[m]["list"] = acceptable_m_prefs
            self.men[m]["rank"] = {woman: idx for idx, woman in enumerate(acceptable_m_prefs)}
            
        for w, w_prefs in self.women.items():
            acceptable_w_prefs = []
            for m in w_prefs["list"]:
                if w in self.men[m]["list"]:
                    acceptable_w_prefs.append(m)
            self.women[w]["list"] = acceptable_w_prefs
            self.women[w]["rank"] = {man: idx for idx, man in enumerate(acceptable_w_prefs)}