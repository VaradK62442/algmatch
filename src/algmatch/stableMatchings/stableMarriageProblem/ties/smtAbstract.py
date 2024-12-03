"""
Stable Marriage Problem With Ties - Abstract class
"""

from copy import deepcopy
import os

from algmatch.stableMatchings.stableMarriageProblem.ties.smtPreferenceInstance import SMTPreferenceInstance


class SMTAbstract:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        assert filename is not None or dictionary is not None, "Either filename or dictionary must be provided"
        assert not (filename is not None and dictionary is not None), "Only one of filename or dictionary must be provided"

        if filename is not None:    
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._reader = SMTPreferenceInstance(filename=filename)

        if dictionary is not None:
            self._reader = SMTPreferenceInstance(dictionary=dictionary)

        self.men = self._reader.men
        self.women = self._reader.women

        self.original_men = deepcopy(self.men)
        self.original_women = deepcopy(self.women)

        self.M = {} # provisional matching
        self.stable_matching = {
            "man_sided": {m: "" for m in self.men},
            "woman_sided": {w: "" for w in self.women}
        }
        self.is_stable = False

    # =======================================================================    
    # Is M stable? Check for blocking pair
    # self.blocking_pair is set to True if blocking pair exists
    # =======================================================================
    def _check_stability(self):      
        # stability must be checked with regards to the original lists prior to deletions  
        for man in self.original_men:
            preferred_women = self.original_men[man]["list"]
            if self.M[man]["assigned"] is not None:
                matched_woman = self.M[man]["assigned"]
                rank_matched_woman = self.original_men[man]["rank"][matched_woman]
                A_mi = self.original_men[man]["list"]
                # every woman that m_i prefers to his matched partner or is indifferent between them
                preferred_women = [wj for wj in A_mi[:rank_matched_woman+1]]  
                # this includes his current partner so we remove her
                preferred_women[-1].remove(matched_woman)                    
        
            for w_tie in preferred_women:
                for woman in w_tie:
                    existing_fiance = self.M[woman]["assigned"]
                    if existing_fiance is None:
                        return False
                    else:
                        rank_fiance = self.original_women[woman]["rank"][existing_fiance]
                        # every man that w_j prefers to her matched partner or is indifferent between them
                        for m_tie in self.original_women[woman]["list"][:rank_fiance+1]:
                            if man in m_tie:
                                return False
        return True

    def _while_loop(self):
        raise NotImplementedError("Method _while_loop must be implemented in subclass")

    def run(self) -> None:
        if self._while_loop():
            for man in self.men:
                woman = self.M[man]["assigned"]
                if woman != set():
                    self.stable_matching["man_sided"][man] = woman

            for woman in self.women:
                man = self.M[woman]["assigned"]
                if man != set():
                    self.stable_matching["woman_sided"][woman] = man

            self.is_stable = True #self._check_stability()

            if self.is_stable:
                return f"super-stable matching: {self.stable_matching}"
        return "no super-stable matching"