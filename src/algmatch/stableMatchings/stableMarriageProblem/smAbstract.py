"""
Stable Marriage Problem - Abstract class
"""

import os

from algmatch.stableMatchings.stableMarriageProblem.smPreferenceInstance import SMPreferenceInstance


class SMAbstract:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        assert filename is not None or dictionary is not None, "Either filename or dictionary must be provided"
        assert not (filename is not None and dictionary is not None), "Only one of filename or dictionary must be provided"

        if filename is not None:    
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._reader = SMPreferenceInstance(filename=filename)

        if dictionary is not None:
            self._reader = SMPreferenceInstance(dictionary=dictionary)

        self.men = self._reader.men
        self.women = self._reader.women

        self.M = {} # provisional matching
        self.stable_matching = {
            "man_sided": {m: "" for m in self.men},
            "woman_sided": {w: "" for w in self.women}
        }

    # =======================================================================    
    # Is M stable? Check for blocking pair
    # self.blocking_pair is set to True if blocking pair exists
    # =======================================================================
    def _check_stability(self) -> bool:        
        for man in self.men:
            preferred_women = self.men[man]["list"]
            if self.M[man]["assigned"] is not None:
                matched_woman = self.M[man]["assigned"]
                rank_matched_woman = self.men[man]["rank"][matched_woman]
                A_mi = self.men[man]["list"]
                preferred_women = [wj for wj in A_mi[:rank_matched_woman]] # every woman that m_i prefers to his matched partner                                
        
            for woman in preferred_women:
                existing_fiance = self.M[woman]["assigned"]
                if existing_fiance == None:
                    return False
                else:
                    rank_fiance = self.women[woman]["rank"][existing_fiance]
                    if man in self.women[woman]["list"][:rank_fiance]:
                        return False
                
        return True

    def _while_loop(self):
        raise NotImplementedError("Method _while_loop must be implemented in subclass")
    

    def run(self) -> None:
        self._while_loop()

        for man in self.men:
            woman = self.M[man]["assigned"]
            if woman is not None:
                self.stable_matching["man_sided"][man] = woman
                self.stable_matching["woman_sided"][woman] = man

        if self._check_stability(): return f"stable matching: {self.stable_matching}"
        else: return f"unstable matching: {self.stable_matching}"
