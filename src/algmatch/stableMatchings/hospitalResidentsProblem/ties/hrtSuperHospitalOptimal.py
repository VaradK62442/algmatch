"""
Algorithm to produce M_0, the hospital-optimal, resident-pessimal super-stable matching, where such a thing exists.
"""

from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtAbstract import (
    HRTAbstract,
)


class HRTSuperHospitalOptimal(HRTAbstract):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(
            filename=filename, dictionary=dictionary, stability_type="super"
        )

        self.undersub_hospitals = set()
        self.been_assigned = {r: False for r in self.residents}

        for resident in self.residents:
            self.M[resident] = {"assigned": set()}

        for hospital, h_prefs in self.hospitals.items():
            if len(h_prefs["list"]) > 0:
                self.undersub_hospitals.add(hospital)
            self.M[hospital] = {"assigned": set()}

    def _delete_pair(self, resident, hospital):
        super()._delete_pair(resident, hospital)
        if self._get_pref_length(hospital) == 0:
            self.undersub_hospitals.discard(hospital)

    def _break_assignment(self, resident, hospital):
        super()._break_assignment(resident, hospital)
        if self._get_pref_length(hospital) == 0:
            self.undersub_hospitals.add(hospital)

    def indifferent_between_assigned_hospitals(self, r):
        r_ranks = self._get_pref_ranks(r)
        return len(set(r_ranks[h] for h in self.M[r]["assigned"])) == 1

    def _while_loop(self) -> bool:
        while len(self.undersub_hospitals) != 0:
            h = self.undersub_hospitals.pop()
            r_tie = self._get_head(h)
            for r in r_tie:
                self._assign(r, h)
                self.been_assigned[r] = True

                if len(self.M[r]["assigned"]) > 1:
                    if self.indifferent_between_assigned_hospitals(r):
                        self._delete_tail(r)
                else:
                    self._reject_lower_ranks(r, h)

        # Check Viability of Matching
        for r in self.residents:
            if len(self.M[r]["assigned"]) == 0 and self.been_assigned[r]:
                return False

        for h in self.hospitals:
            capacity = self.hospitals[h]["capacity"]
            occupancy = len(self.M[h]["assigned"])
            if occupancy > capacity:
                return False

        return True
