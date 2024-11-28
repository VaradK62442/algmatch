"""
Hospital/Residents Problem - Abstract class
"""

from copy import deepcopy
import os

from algmatch.stableMatchings.hospitalResidentsProblem.hrPreferenceInstance import HRPreferenceInstance


class HRAbstract:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        assert filename is not None or dictionary is not None, "Either filename or dictionary must be provided"
        assert not (filename is not None and dictionary is not None), "Only one of filename or dictionary must be provided"

        if filename is not None:    
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._reader = HRPreferenceInstance(filename=filename)

        if dictionary is not None:
            self._reader = HRPreferenceInstance(dictionary=dictionary)

        self.residents = self._reader.residents
        self.hospitals = self._reader.hospitals

        # we need original copies of the preference lists to check the stability of solutions
        self.original_residents = deepcopy(self.residents)
        self.original_hospitals = deepcopy(self.hospitals)

        self.M = {} # provisional matching
        self.stable_matching = {
            "resident_sided": {resident: "" for resident in self.residents},
            "hospital_sided": {hospital: [] for hospital in self.hospitals}
        }
        self.is_stable = False

    def _blocking_pair_condition(self, resident, hospital):
        # blocking pairs exist w.r.t the original preference lists; we must use original_
        # capacity doesn't change but I'm using original_hospitals here for consistency in this function.
        cj = self.original_hospitals[hospital]["capacity"]
        occupancy = len(self.M[hospital]["assigned"])
        if occupancy < cj:
            return True
        
        resident_rank = self.original_hospitals[hospital]["rank"][resident]
        for existing_resident in self.M[hospital]["assigned"]:
            existing_rank = self.original_hospitals[hospital]["rank"][existing_resident]
            if resident_rank < existing_rank:
                return True
            
        return False

    def _check_stability(self):
        # stability must be checked with regards to the original lists prior to deletions       
        for resident in self.original_residents:
            preferred_hospitals = self.original_residents[resident]["list"]
            if self.M[resident]["assigned"] is not None:
                matched_hospital = self.M[resident]["assigned"]
                rank_matched_hospital = self.original_residents[resident]["rank"][matched_hospital]
                A_ri = self.original_residents[resident]["list"]
                preferred_hospitals = [hj for hj in A_ri[:rank_matched_hospital]]                             
        
            for hospital in preferred_hospitals:
                if self._blocking_pair_condition(resident, hospital):
                    return False
                
        return True

    def _while_loop(self):
        raise NotImplementedError("Method _while_loop must be implemented in subclass")

    def run(self) -> None:
        self._while_loop()

        for resident in self.residents:
            hospital = self.M[resident]["assigned"]
            if hospital is not None:
                self.stable_matching["resident_sided"][resident] = hospital
                self.stable_matching["hospital_sided"][hospital].append(resident)

        self.is_stable = self._check_stability()

        if self.is_stable:
            return f"stable matching: {self.stable_matching}"
        else:
            return f"unstable matching: {self.stable_matching}"
