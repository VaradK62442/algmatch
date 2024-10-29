"""
Store preference lists for Hospital/Residents Problem stbale matching algorithm.
"""

from abstractClasses.abstractPreferenceInstance import AbstractPreferenceInstance
from stableMatchings.hospitalResidentsProblem.fileReader import FileReader
from stableMatchings.hospitalResidentsProblem.dictionaryReader import DictionaryReader


class HRPreferenceInstance(AbstractPreferenceInstance):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        super().__init__(filename, dictionary)

    def _load_from_file(self, filename: str) -> None:
        reader = FileReader(filename)
        self.residents = reader.residents
        self.hospitals = reader.hospitals

    def _load_from_dictionary(self, dictionary: dict) -> None:
        reader = DictionaryReader(dictionary)
        self.residents = reader.residents
        self.hospitals = reader.hospitals