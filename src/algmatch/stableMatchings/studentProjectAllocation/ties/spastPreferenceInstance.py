"""
Store preference lists for student project allocation with ties algorithm.
"""

from algmatch.abstractClasses.abstractPreferenceInstance import AbstractPreferenceInstance
from algmatch.stableMatchings.studentProjectAllocation.ties.fileReader import FileReader
from algmatch.stableMatchings.studentProjectAllocation.ties.dictionaryReader import DictionaryReader


class SPAPreferenceInstance(AbstractPreferenceInstance):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        super().__init__(filename, dictionary)

    def _load_from_file(self, filename: str) -> None:
        reader = FileReader(filename)
        self.students = reader.students
        self.projects = reader.projects
        self.lecturers = reader.lecturers

    def _load_from_dictionary(self, dictionary: dict) -> None:
        reader = DictionaryReader(dictionary)
        self.students = reader.students
        self.projects = reader.projects
        self.lecturers = reader.lecturers