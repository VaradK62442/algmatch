"""
Class to read in a file of preferences for the Stable Marriage Problem stable matching algorithm.
"""
from itertools import product

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.abstractClasses.abstractReader import ReaderError


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def check_preference_lists(self) -> None:
        for m, m_prefs in self.men.items():

            if len(set(m_prefs["list"])) != len(m_prefs["list"]):
                raise ReaderError(f"man {m}", "Repetition in preference list.")
            
            for w in m_prefs["list"]:
                if w not in self.women:
                    raise ReaderError(f"man {m}", f"Woman {w} not instantiated.")
            
        for w, w_prefs in self.women.items():

            if len(set(w_prefs["list"])) != len(w_prefs["list"]):
                raise ReaderError(f"woman {w}", "Repetition in preference list.")
            
            for m in w_prefs["list"]:
                if m not in self.men:
                    raise ReaderError(f"woman {w}", f"Man {m} not instantiated.")

    def clean_unacceptable_pairs(self) -> None:
        for m, w in product(self.men, self.women):
            if m not in self.women[w]["list"] or w not in self.men[m]["list"]:
                try: m.remove(w)
                except ValueError: pass
                try: w.remove(m)
                except ValueError: pass

    def set_up_rankings(self):
        for m in self.men:
            self.men[m]["rank"] = {woman: idx for idx, woman in enumerate(self.men[m]["list"])}
        for w in self.women:
            self.women[w]["rank"] = {man: idx for idx, man in enumerate(self.women[w]["list"])}
    
    def parse_file(self) -> None:
        self.no_men = 0
        self.no_women = 0
        self.men = {}                
        self.women = {}
        cur_line = 1
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        try:
            self.no_men, self.no_women = map(int, file[0].split())
        except ValueError:
            raise ReaderError(cur_line, "Participant Quantities Misformatted")

        # build men dictionary
        for elt in file[1:self.no_men+1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise ReaderError(f"line {cur_line}", "Man ID misformatted")
            man = f"m{entry[0]}"
            if man in self.men:
                raise ReaderError(f"line {cur_line}", "Repeated man ID")

            for i in entry[1:]:
                if not i.isdigit():
                    raise ReaderError(f"line {cur_line}", "Man preference list misformatted")
            preferences = [f"w{i}" for i in entry[1:]]

            self.men[man] = {"list": preferences, "rank": {}}

        # build women dictionary
        for elt in file[self.no_men+1:self.no_men+self.no_women+1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise ReaderError(f"line {cur_line}", "Woman ID misformatted")
            woman = f"w{entry[0]}"
            if woman in self.women:
                raise ReaderError(f"line {cur_line}", "Repeated woman ID")

            for i in entry[1:]:
                if not i.isdigit():
                    raise ReaderError(f"line {cur_line}", "Woman preference list misformatted")
            preferences = [f"m{i}" for i in entry[1:]]

            self.women[woman] = {"list": preferences, "rank": {}}
    
    def _read_data(self) -> None:
        self.parse_file()
        self.check_preference_lists()
        self.clean_unacceptable_pairs()
        self.set_up_rankings()