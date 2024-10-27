"""
Store preference lists for Stable Roommates stable matching algorithm.
"""

from abstractClasses.abstractPreferenceInstance import AbstractPreferenceInstance
from stableMatchings.stableRoommates.fileReader import FileReader
from stableMatchings.stableRoommates.dictionaryReader import DictionaryReader


class SRPreferenceInstance(AbstractPreferenceInstance):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        super().__init__(filename, dictionary)

    def _load_from_file(self, filename: str) -> None:
        reader = FileReader(filename)
        self.roommates = reader.roommates

    def _load_from_dictionary(self, dictionary: dict) -> None:
        reader = DictionaryReader(dictionary)
        self.roommates = reader.roommates