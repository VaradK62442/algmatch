"""
Class to read in a dictionary of preferences for the Student Project Allocation stable matching algorithm.
"""
from itertools import product


from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.abstractClasses.abstractReader import ReaderError

class DictionaryReader(AbstractReader):
    def __init__(self, dictionary: dict) -> None:
        super().__init__(dictionary)
        self._read_data()

    def parse_dictionary(self) -> None:
        self.men = {}
        self.women = {}

        for key, value in self.data.items():
            match key:
                case "men":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise ReaderError(f"man {k}", "Man ID misformatted")
                        man = f"m{k}"
                        if man in self.men:
                            raise ReaderError(f"man {k}", "Repeated man ID")
                        preferences = [f"w{i}" for i in v]

                        self.men[man] = {"list": preferences, "rank": {}}

                case "women":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise ReaderError(f"woman {k}", "Woman ID misformatted")
                        woman = f"w{k}"
                        if woman in self.women:
                            raise ReaderError(f"woman {k}", "Repeated woman ID")
                        preferences = [f"m{i}" for i in v]

                        self.women[woman] = {"list": preferences, "rank": {}}

    def set_up_rankings(self):
        for m in self.men:
            self.men[m]["rank"] = {woman: idx for idx, woman in enumerate(self.men[m]["list"])}
        for w in self.women:
            self.women[w]["rank"] = {man: idx for idx, man in enumerate(self.women[w]["list"])}

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

    def _read_data(self) -> None:
        self.parse_dictionary()
        self.check_preference_lists()
        self.clean_unacceptable_pairs()
        self.set_up_rankings()