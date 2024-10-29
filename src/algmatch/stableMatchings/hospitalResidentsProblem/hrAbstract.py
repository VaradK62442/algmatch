"""
Hospital/Residents Problem - Abstract class
"""

import os

from stableMatchings.hospitalResidentsProblem.hrPreferenceInstance import HRPreferenceInstance


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

        self.M = {} # provisional matching
        self.stable_matching = {}
        self.blocking_pair = False

    def _blocking_pair_condition(self, resident, hospital):
        cj = self.hospitals[hospital]["capacity"]
        occupancy = len(self.M[hospital]["assigned"])
        if occupancy < cj:
            return True
        
        resident_rank = self.hospitals[hospital]["rank"][resident]
        for existing_resident in self.M[hospital]["assigned"]:
            existing_rank = self.hospitals[hospital]["rank"][existing_resident]
            if resident_rank < existing_rank:
                return True
            
        return False

    # =======================================================================    
    # Is M stable? Check for blocking pair
    # self.blocking_pair is set to True if blocking pair exists
    # =======================================================================
    def _check_stability(self):        
        for resident in self.residents:
            preferred_hospitals = self.residents[resident]["list"]
            if self.M[resident]["assigned"] is not None:
                matched_hospital = self.M[resident]["assigned"]
                rank_matched_hospital = self.residents[resident]["rank"][matched_hospital]
                A_ri = self.residents[resident]["list"]
                preferred_hospitals = [hj for hj in A_ri[:rank_matched_hospital]] # every project that s_i prefers to her matched project                                
        
            for hospital in preferred_hospitals:
                if not self.blocking_pair:
                    self.blocking_pair = self._blocking_pair_condition(resident, hospital)
                
                if self.blocking_pair:
                #    print(student, project, lecturer)
                   break
            
            if self.blocking_pair:
                # print(student, project, lecturer)
                break


    def _while_loop(self):
        raise NotImplementedError("Method _while_loop must be implemented in subclass")
    

    def run(self) -> None:
        self._while_loop()
        self._check_stability()

        for resident in self.residents:
            if self.M[resident]["assigned"] is not None:
                self.stable_matching[resident] = self.M[resident]["assigned"]
            else:
                self.stable_matching[resident] = ""

        if not self.blocking_pair:
            return f"stable matching: {self.stable_matching}"
        else: return f"unstable matching: {self.stable_matching}"