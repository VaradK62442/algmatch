"""
Algorithm to produce M_0, the man-optimal, woman-pessimal stable matching, where such a thing exists.
"""

import os
from copy import deepcopy

from stableMatchings.stableMarriageProblem.smAbstract import SMAbstract

class SMManOptimal(SMAbstract):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        super().__init__(filename=filename, dictionary=dictionary)

        for man in self.men:
            self.M[man] = {"assigned": None}

        for woman in self.women:
            self.M[woman] = {"assigned": None}

    def _delete(self, man, woman):
        self.men[man]['list'].remove(woman)
        self.women[woman]['list'].remove(man)
 
    def _while_loop(self):
        while False:
            pass