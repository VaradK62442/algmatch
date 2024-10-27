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
                        rank = {woman: idx for idx, woman in enumerate(preferences)}

                        self.men[man] = {"list": preferences, "rank": rank}

                case "women":
                    for k, v in value.items():
                        woman = f"w{k}"
                        preferences = [f"m{i}" for i in v]
                        rank = {man: idx for idx, man in enumerate(preferences)}

                        self.women[woman] = {"list": preferences, "rank": rank}