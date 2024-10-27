"""
Stable Roomates - Abstract class
"""

import os

from stableMatchings.stableRoommates.srPreferenceInstance import SRPreferenceInstance


class SRAbstract:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        assert filename is not None or dictionary is not None, "Either filename or dictionary must be provided"
        assert not (filename is not None and dictionary is not None), "Only one of filename or dictionary must be provided"

        if filename is not None:    
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._reader = SRPreferenceInstance(filename=filename)

        if dictionary is not None:
            self._reader = SRPreferenceInstance(dictionary=dictionary)

        self.roommates = self._reader.roommates

        self.M = {} # provisional matching
        self.stable_matching = {}
        self.blocking_pair = False

    # =======================================================================    
    # Is M stable? Check for blocking pair
    # self.blocking_pair is set to True if blocking pair exists
    # =======================================================================
    def _check_stability(self):        
        for x in self.roommates:
            preferred_by_x = self.roommates[x]["list"]
            if self.M[x]["assigned"] is not None:
                match = self.M[x]["assigned"]
                rank_match = self.roommates[x]["rank"][match]
                A_x = self.roommates[x]["list"]
                preferred_by_x = [ri for ri in A_x[:rank_match]] # every woman that m_i prefers to his matched partner                                
        
            for y in preferred_by_x:
                z = self.M[y]["assigned"]
                if z == None:
                    self.blocking_pair = True
                else:
                    rank_z = self.women[y]["rank"][z]
                    if z in self.women[y]["list"][:rank_z]:
                        self.blocking_pair = True
                
                if self.blocking_pair:
                    # print(man, woman)
                    break
            
            if self.blocking_pair:
                # print(man, woman)
                break

    def _while_loop(self):
        raise NotImplementedError("Method _while_loop must be implemented in subclass")
    

    def run(self) -> None:
        self._while_loop()
        self._check_stability()

        for roommate in self.roommates:
            if self.M[roommate]["assigned"] is not None:
                self.stable_matching[roommate] = self.M[roommate]["assigned"]
            else:
                self.stable_matching[roommate] = ""

        if not self.blocking_pair:
            return f"stable matching: {self.stable_matching}"
        else: return f"unstable matching: {self.stable_matching}"