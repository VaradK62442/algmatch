"""
Stable Marriage Problem With Ties - Abstract class
"""

from copy import deepcopy
import os

from algmatch.stableMatchings.stableMarriageProblem.ties.smtPreferenceInstance import SMTPreferenceInstance


class SMTAbstract:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None, stability_type: str = None) -> None:
        assert filename is not None or dictionary is not None, "Either filename or dictionary must be provided"
        assert not (filename is not None and dictionary is not None), "Only one of filename or dictionary must be provided"
        
        self.assert_valid_stability_type(stability_type)
        self.stability_type = stability_type.lower()

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

    def assert_valid_stability_type(self, st):
        assert st is not None, "Select a stability type - either 'super' or 'strong'"
        assert type(st) is str, "Stability type is not str'"
        assert st.lower() in ("super", "strong"), "Stability type must be either 'super' or 'strong'"

    # =======================================================================    
    # Is M stable? Check for blocking pair
    # self.blocking_pair is set to True if blocking pair exists
    # =======================================================================
    def _check_super_stability(self):      
        # stability must be checked with regards to the original lists prior to deletions  
        for man, m_prefs in self.original_men.items():
            preferred_women = self.original_men[man]["list"]
            if self.M[man]["assigned"] is not None:
                matched_woman = self.M[man]["assigned"]
                rank_matched_woman = m_prefs["rank"][matched_woman]
                # every woman that m_i prefers to his matched partner or is indifferent between them
                preferred_women = m_prefs["list"][:rank_matched_woman+1]  
                # this includes his current partner so we remove her
                preferred_women[-1].remove(matched_woman)                    
        
            for w_tie in preferred_women:
                for woman in w_tie:
                    existing_fiance = self.M[woman]["assigned"]
                    if existing_fiance is None:
                        return False
                    else:
                        w_prefs = self.original_women[woman]
                        rank_fiance = w_prefs["rank"][existing_fiance]
                        rank_man = w_prefs["rank"][man]
                        if rank_man >= rank_fiance:
                            return False
        return True
    
    def _check_strong_stability(self):
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

            if self.stability_type == "super":
                self.is_stable = self._check_super_stability()
            else:
                self.is_stable = self._check_strong_stability()

            if self.is_stable:
                return f"super-stable matching: {self.stable_matching}"
        return "no super-stable matching"