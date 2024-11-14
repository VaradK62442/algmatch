"""
Store preference lists for Stable Marriage stable matching algorithm.
"""
from itertools import product

from algmatch.abstractClasses.abstractPreferenceInstance import AbstractPreferenceInstance
from algmatch.stableMatchings.stableMarriageProblem.fileReader import FileReader
from algmatch.stableMatchings.stableMarriageProblem.dictionaryReader import DictionaryReader
from algmatch.abstractClasses.abstractReader import ReaderError

class SMPreferenceInstance(AbstractPreferenceInstance):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        super().__init__(filename, dictionary)
        self.check_preference_lists()
        self.clean_unacceptable_pairs()
        self.set_up_rankings()

    def _load_from_file(self, filename: str) -> None:
        reader = FileReader(filename)
        self.men = reader.men
        self.women = reader.women

    def _load_from_dictionary(self, dictionary: dict) -> None:
        reader = DictionaryReader(dictionary)
        self.men = reader.men
        self.women = reader.women

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
    
example = {
    'men': {
        1: [2, 4, 1, 3],
        2: [3, 1, 4, 2],
        3: [2, 3, 1, 4],
        4: [4, 1, 3, 2]
    },
    'women': {
        1: [2, 1, 4, 3],
        2: [4, 3, 1, 2],
        3: [1, 4, 3, 2],
        4: [2, 1, 4, 3]
    }
}
ins = SMPreferenceInstance(dictionary=example)