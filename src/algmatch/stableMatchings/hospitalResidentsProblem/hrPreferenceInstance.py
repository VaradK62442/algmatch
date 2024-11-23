"""
Store preference lists for Hospital/Residents Problem stbale matching algorithm.
"""
from itertools import product

from algmatch.abstractClasses.abstractPreferenceInstance import AbstractPreferenceInstance
from algmatch.stableMatchings.hospitalResidentsProblem.fileReader import FileReader
from algmatch.stableMatchings.hospitalResidentsProblem.dictionaryReader import DictionaryReader
from algmatch.errors.InstanceSetupErrors import PrefRepError, PrefNotFoundError

class HRPreferenceInstance(AbstractPreferenceInstance):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        super().__init__(filename, dictionary)
        self.check_preference_lists()
        self.clean_unacceptable_pairs()
        self.set_up_rankings()

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
                raise PrefRepError("resident",r)
            
            for h in r_prefs["list"]:
                if h not in self.hospitals:
                    raise PrefNotFoundError("resident",r,h)
            
        for h, h_prefs in self.hospitals.items():

            if len(set(h_prefs["list"])) != len(h_prefs["list"]):
                raise PrefRepError("hospital",h)
            
            for r in h_prefs["list"]:
                if r not in self.residents:
                    raise PrefNotFoundError("hospital",h,r)
                
    def clean_unacceptable_pairs(self) -> None:
        for r, h in product(self.residents, self.hospitals):
            if r not in self.hospitals[h]["list"] or h not in self.residents[r]["list"]:
                try:
                    self.residents[r]["list"].remove(h)
                except ValueError:
                    pass
                try:
                    self.hospitals[h]["list"].remove(r)
                except ValueError:
                    pass

    def set_up_rankings(self):
        for r in self.residents:
            self.residents[r]["rank"] = {hospital: idx for idx, hospital in enumerate(self.residents[r]["list"])}
        for h in self.hospitals:
            self.hospitals[h]["rank"] = {resident: idx for idx, resident in enumerate(self.hospitals[h]["list"])}