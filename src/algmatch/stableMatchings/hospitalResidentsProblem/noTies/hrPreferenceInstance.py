"""
Store preference lists for Hospital/Residents Problem stbale matching algorithm.
"""

from algmatch.abstractClasses.abstractPreferenceInstance import (
    AbstractPreferenceInstance,
)
from algmatch.stableMatchings.hospitalResidentsProblem.noTies.fileReader import FileReader
from algmatch.stableMatchings.hospitalResidentsProblem.noTies.dictionaryReader import (
    DictionaryReader,
)


class HRPreferenceInstance(AbstractPreferenceInstance):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(filename, dictionary)
        self._general_setup_procedure()

    def _load_from_file(self, filename: str) -> None:
        reader = FileReader(filename)
        self.residents = reader.residents
        self.hospitals = reader.hospitals

    def _load_from_dictionary(self, dictionary: dict) -> None:
        reader = DictionaryReader(dictionary)
        self.residents = reader.residents
        self.hospitals = reader.hospitals

    def check_preference_lists(self) -> None:
        self.check_preferences_single_group(self.residents, "resident", self.hospitals)
        self.check_preferences_single_group(self.hospitals, "hospital", self.residents)

    def clean_unacceptable_pairs(self) -> None:
        super().clean_unacceptable_pairs(self.residents, self.hospitals)

    def set_up_rankings(self) -> None:
        self.tieless_lists_to_rank(self.residents)
        self.tieless_lists_to_rank(self.hospitals)
