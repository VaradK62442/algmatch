"""
Algorithm to produce M_z, the woman-optimal, man-pessimal super-stable matching, where such a thing exists.
"""

from algmatch.stableMatchings.stableMarriageProblem.ties.smtAbstract import SMTAbstract
from algmatch.stableMatchings.stableMarriageProblem.ties.graphMax import GraphMax


class SMTSuperWomanOriented(SMTAbstract):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(
            filename=filename, dictionary=dictionary, stability_type="super"
        )

        self.unassigned_women = set()
        self.proposed = {m: False for m in self.men}

        for man, prefs in self.men.items():
            self.M[man] = {"assigned": set()}

        for woman in self.women:
            if len(prefs["list"]) > 0:
                self.unassigned_women.add(woman)
            self.M[woman] = {"assigned": set()}

    def _delete_pair(self, man, woman) -> None:
        super()._delete_pair(man, woman)
        if man in self.women:
            man, woman = woman, man
        if self._get_pref_length(woman) == 0:
            self.unassigned_women.discard(woman)

    def _break_assignment(self, man, woman):
        super()._break_assignment(man, woman)
        if woman in self.men:
            man, woman, woman, man
        if self._get_pref_length(woman) > 0:
            self.unassigned_women.add(woman)

    def _while_loop(self) -> bool:
        while len(self.unassigned_women) != 0:
            while len(self.unassigned_women) != 0:
                w = self.unassigned_women.pop()
                m_tie = self._get_head(w)
                for m in m_tie:
                    self._engage(m, w)
                    self.proposed[m] = True
                    self._reject_lower_ranks(m, w)

            for m in self.men:
                if len(self.M[m]["assigned"]) > 1:
                    self._break_all_engagements(m)
                    self._delete_tail(m)

        # do flow alg to get max matching
        graph_maxer = GraphMax(self.M)
        self.M = graph_maxer.get_max_matching()

        # check viability of matching
        for m in self.men:
            if self.M[m]["assigned"] is None and self.proposed[m]:
                return False
        return True
