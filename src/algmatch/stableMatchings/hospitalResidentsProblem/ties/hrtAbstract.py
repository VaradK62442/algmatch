"""
Stable Marriage Problem With Ties - Abstract class
"""

from copy import deepcopy
import os

from algmatch.stableMatchings.stableMarriageProblem.ties.smtPreferenceInstance import SMTPreferenceInstance
from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtPreferenceInstance import HRTPreferenceInstance


class HRTAbstract:
    def __init__(self,
                 filename: str | None = None,
                 dictionary: dict | None = None,
                 stability_type: str = None) -> None:
        
        assert filename is not None or dictionary is not None, "Either filename or dictionary must be provided"
        assert not (filename is not None and dictionary is not None), "Only one of filename or dictionary must be provided"
        
        self.assert_valid_stability_type(stability_type)
        self.stability_type = stability_type.lower()

        if filename is not None:    
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._reader = SMTPreferenceInstance(filename=filename)

        if dictionary is not None:
            self._reader = SMTPreferenceInstance(dictionary=dictionary)

        self.residents = self._reader.residents
        self.hospitals = self._reader.hospitals

        self.original_residents = deepcopy(self.residents)
        self.original_hosptials = deepcopy(self.hospitals)

        self.M = {} # provisional matching
        self.stable_matching = {
            "resident_sided": {r: "" for r in self.residents},
            "hospital_sided": {h: set() for h in self.hospitals}
        }
        self.is_stable = False

    def assert_valid_stability_type(self, st) -> None:
        assert st is not None, "Select a stability type - either 'super' or 'strong'"
        assert type(st) is str, "Stability type is not str'"
        assert st.lower() in ("super", "strong"), "Stability type must be either 'super' or 'strong'"

    def _check_super_stability(self) -> bool:      
        raise NotImplementedError("Super-stability checking isn't implemented")
    
    def _check_strong_stability(self) -> bool:
        raise NotImplementedError("Strong stability checking isn't implemented")

    def _while_loop(self) -> bool:
        raise NotImplementedError("Method _while_loop must be implemented in subclass")

    def save_resident_sided(self) -> None:
        raise NotImplementedError("Method save_resident_sided not yet implemented")

    def save_hospital_sided(self) -> None:
        raise NotImplementedError("MMethod save_hospital_sided not yet implemented")

    def run(self) -> None:
        if self._while_loop():
            
            self.save_man_sided()
            self.save_woman_sided()

            if self.stability_type == "super":
                self.is_stable = self._check_super_stability()
            else:
                self.is_stable = self._check_strong_stability()

            if self.is_stable:
                return f"super-stable matching: {self.stable_matching}"
        return "no super-stable matching"