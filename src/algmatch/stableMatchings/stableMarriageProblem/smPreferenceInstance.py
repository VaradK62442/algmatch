"""
Store preference lists for Stable Marriage stable matching algorithm.
"""

from algmatch.abstractClasses.abstractPreferenceInstance import AbstractPreferenceInstance
from algmatch.stableMatchings.stableMarriageProblem.fileReader import FileReader
from algmatch.stableMatchings.stableMarriageProblem.dictionaryReader import DictionaryReader


class SMPreferenceInstance(AbstractPreferenceInstance):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        super().__init__(filename, dictionary)

    def _load_from_file(self, filename: str) -> None:
        reader = FileReader(filename)
        self.men = reader.men
        self.women = reader.women

    def _load_from_dictionary(self, dictionary: dict) -> None:
        reader = DictionaryReader(dictionary)
        self.men = reader.men
        self.women = reader.women