"""
Class to read in a dictionary of preferences for the Stable Marriage Problem stable matching algorithm.
"""

from abstractClasses.abstractReader import AbstractReader


class DictionaryReader(AbstractReader):
    def __init__(self, dictionary: dict) -> None:
        super().__init__(dictionary)
        self._read_data()

    def _read_data(self) -> None:
        self.men = {}
        self.women = {}

        for key, value in self.data.items():
            match key:
                case "men":
                    for k, v in value.items():
                        man = f"m{k}"
                        preferences = [f"w{i}" for i in v]

                        self.men[man] = {"list": preferences, "rank": {}}

                case "women":
                    for k, v in value.items():
                        woman = f"w{k}"
                        preferences = [f"m{i}" for i in v]

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