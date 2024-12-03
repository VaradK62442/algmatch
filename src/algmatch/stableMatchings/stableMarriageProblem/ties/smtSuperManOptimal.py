"""
Algorithm to produce M_0, the man-optimal, woman-pessimal super-stable matching, where such a thing exists.
"""

from algmatch.stableMatchings.stableMarriageProblem.ties.smtAbstract import SMTAbstract
from algmatch.stableMatchings.stableMarriageProblem.ties.smGraphMax import SMGraphMax

class SMTSuperManOptimal(SMTAbstract):
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        super().__init__(filename=filename, dictionary=dictionary)

        self.unassigned_men = set()
        self.proposed = {w : False for w in self.women}

        for man, prefs in self.men.items():
            if len(prefs["list"]) > 0:
                self.unassigned_men.add(man)
            self.M[man] = {"assigned": set()}

        for woman in self.women:
            self.M[woman] = {"assigned": set()}

    def _get_pref_length(self,man):
        pref_sets = self.men[man]["list"]
        total = sum([len(s) for s in pref_sets])
        return total

    def _get_head(self,pref_list):
        idx = 0
        while idx < len(pref_list):
            head = pref_list[idx]
            if len(head) > 0:
                return head
            idx += 1
        raise ValueError("Pref_list empty")
    
    def _get_tail(self,pref_list):
        idx = len(pref_list)-1
        while idx >= 0:
            tail = pref_list[idx]
            if len(tail) > 0:
                return tail
            idx -= 1
        raise ValueError("Pref_list empty")

    def _delete_pair(self, man, woman):
        for tie in  self.men[man]['list']:
            tie.discard(woman)
        for tie in  self.women[woman]['list']:
            tie.discard(man)
        if self._get_pref_length(man) == 0:
            self.unassigned_men.discard(man)

    def _delete_tail(self,woman):
        tail = self._get_tail(self.women[woman]["list"])
        while len(tail) != 0:
            man = tail.pop()
            self._delete_pair(man,woman)

    def _engage(self, man, woman):
        self.M[man]["assigned"].add(woman)
        self.M[woman]["assigned"].add(man)

    def _break_engagement(self, man, woman):
        self.M[man]["assigned"].discard(woman)
        self.M[woman]["assigned"].discard(man)

    def _break_all_engagements(self,woman):
        men_assigned = self.M[woman]["assigned"]
        while len(men_assigned) != 0:
            man = men_assigned.pop()
            self._break_engagement(man,woman)
 
    def _while_loop(self) -> bool:
        while True:
            while len(self.unassigned_men) != 0:

                m = self.unassigned_men.pop()
                w_tie = self._get_head(self.men[m]["list"])
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
                if len(self.M[m]["assigned"]) > 0:
                    pass
                elif self._get_pref_length(m) == 0:
                    pass
                else:
                    end_condition = False
            if end_condition:
                break
        
        # do flow alg to get max matching
        graph_maxer = SMGraphMax(self.M)
        M_prime = graph_maxer.get_max_matching()

        # check viability of matching
        for w in self.women:
            if self.M_prime[w]["assigned"] == None and self.proposed[w]:
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
