"""
Algorithm to produce M_0, the man-optimal, woman-pessimal super-stable matching, where such a thing exists.
"""

from algmatch.stableMatchings.stableMarriageProblem.ties.smtAbstract import SMTAbstract
from algmatch.stableMatchings.stableMarriageProblem.ties.graphMax import GraphMax

class SMTSuperManOptimal(SMTAbstract):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
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

    def _delete_pair(self, man, woman):
        super()._delete_pair(self,man,woman)
        if self._get_pref_length(man) == 0:
            self.unassigned_men.discard(man)
 
    def _while_loop(self) -> bool:
        while True:
            while len(self.unassigned_men) != 0:

                m = self.unassigned_men.pop()
                w_tie = self._get_head(m)
                for w in w_tie:
                    self._engage(m,w)
                    self.proposed[w] = True

                    rank_m = self.women[w]["rank"][m]
                    for reject_tie in self.women[w]["list"][rank_m+1:]:
                        while len(reject_tie) != 0:
                            reject = reject_tie.pop()
                            self._break_engagement(reject,w)
                            self._delete_pair(reject,w)

            for w in self.women:
                if len(self.M[w]["assigned"]) > 1:
                    self._break_all_engagements(w)
                    self._delete_tail(w)

            end_condition = True
            for m in self.men:
                if len(self.M[m]["assigned"]) == 0:
                    pass
                elif self._get_pref_length(m) > 0:
                    pass
                else:
                    end_condition = False
            if end_condition:
                break
        
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
