"""
Algorithm to produce M_0, the man-optimal, woman-pessimal super-stable matching, where such a thing exists.
"""

from algmatch.stableMatchings.stableMarriageProblem.ties.smtAbstract import SMTAbstract
from algmatch.stableMatchings.stableMarriageProblem.ties.graphMax import GraphMax

class SMTSuperManOptimal(SMTAbstract):
    def __init__(self,
                 filename: str | None = None,
                 dictionary: dict | None = None) -> None:
        
        super().__init__(filename=filename,
                         dictionary=dictionary,
                         stability_type="super")

        self.unassigned_men = set()
        self.proposed = {w : False for w in self.women}

        for man, prefs in self.men.items():
            if len(prefs["list"]) > 0:
                self.unassigned_men.add(man)
            self.M[man] = {"assigned": set()}

        for woman in self.women:
            self.M[woman] = {"assigned": set()}

    def _delete_pair(self, man, woman) -> None:
        super()._delete_pair(man, woman)
        if self._get_pref_length(man) == 0:
            self.unassigned_men.discard(man)

    def _while_loop(self) -> bool:
        while len(self.unassigned_men) != 0:
            
            while len(self.unassigned_men) != 0:
                m = self.unassigned_men.pop()
                w_tie = self._get_head(m)
                for w in w_tie:
                    self._engage(m,w)
                    self.proposed[w] = True
                    self._reject_lower_ranks(w,m)

            for w in self.women:
                if len(self.M[w]["assigned"]) > 1:
                    self._break_all_engagements(w)
                    self._delete_tail(w)

        # do flow alg to get max matching
        graph_maxer = GraphMax(self.M)
        self.M = graph_maxer.get_max_matching()

        # check viability of matching
        for w in self.women:
            if self.M[w]["assigned"] is None and self.proposed[w]:
                return False
        return True

instance = {
    "men": {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [3, 2, 1]
    },
    "women": {
        1: [1, 2, 3],
        2: [2, 1, 3],
        3: [3, 1, 2]
    }
}

smt_sup_mo = SMTSuperManOptimal(dictionary=instance)
print(smt_sup_mo.run()) 
