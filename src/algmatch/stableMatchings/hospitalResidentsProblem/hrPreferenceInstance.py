"""
Store preference lists for Hospital/Residents Problem stbale matching algorithm.
"""

from algmatch.abstractClasses.abstractPreferenceInstance import (
    AbstractPreferenceInstance,
)
from algmatch.stableMatchings.hospitalResidentsProblem.fileReader import FileReader
from algmatch.stableMatchings.hospitalResidentsProblem.dictionaryReader import (
    DictionaryReader,
)
from algmatch.errors.InstanceSetupErrors import PrefRepError, PrefNotFoundError


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
        for r, r_prefs in self.residents.items():
            if len(set(r_prefs["list"])) != len(r_prefs["list"]):
                raise PrefRepError("resident", r)

            for h in r_prefs["list"]:
                if h not in self.hospitals:
                    raise PrefNotFoundError("resident", r, h)

        for h, h_prefs in self.hospitals.items():
            if len(set(h_prefs["list"])) != len(h_prefs["list"]):
                raise PrefRepError("hospital", h)

            for r in h_prefs["list"]:
                if r not in self.residents:
                    raise PrefNotFoundError("hospital", h, r)

    def clean_unacceptable_pairs(self) -> None:
        super().clean_unacceptable_pairs(self.residents, self.hospitals)

    def set_up_rankings(self):
        self.tieless_lists_to_rank(self.residents)
        self.tieless_lists_to_rank(self.hospitals)
