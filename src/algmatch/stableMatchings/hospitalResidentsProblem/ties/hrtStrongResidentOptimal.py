"""
Algorithm to produce M_0, the resident-optimal, hospital-pessimal super-stable matching, where such a thing exists.
"""

from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtStrongAbstract import (
    HRTStrongAbstract,
)


class HRTStrongResidentOptimal(HRTStrongAbstract):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(filename=filename, dictionary=dictionary)

        self.unassigned_residents = set()
        self.been_full = {h: False for h in self.hospitals}

        for resident, r_prefs in self.residents.items():
            if len(r_prefs["list"]) > 0:
                self.unassigned_residents.add(resident)
            self.M[resident] = {"assigned": set()}

        for hospital in self.hospitals:
            self.M[hospital] = {"assigned": set()}

    def _delete_pair(self, resident, hospital):
        super()._delete_pair(resident, hospital)
        if resident in self.hospitals:
            resident, hospital = hospital, resident
        if self._get_pref_length(resident) == 0:
            self.unassigned_residents.discard(resident)

    def _break_assignment(self, resident, hospital):
        super()._break_assignment(resident, hospital)
        if resident in self.hospitals:
            resident, hospital = hospital, resident
        if self._get_pref_length(resident) > 0:
            self.unassigned_residents.add(resident)

    def _form_G_r(self):
        raise NotImplementedError()

    def _while_loop(self) -> bool:
        Z = {None}
        while Z:
            while len(self.unassigned_residents) != 0:
                r = self.unassigned_residents.pop()
                h_tie = self._get_head(r)
                for h in h_tie.copy():
                    self._assign(r, h)

                    capacity = self.hospitals[h]["capacity"]
                    occupancy = len(self.M[h]["assigned"])
                    if occupancy >= capacity:
                        self._delete_dominated_residents(h)

            self._form_G_r()
            Z = self._get_critical_set()
            for h in self._neighbourhood(Z):
                self._delete_tail(h)

        # Check Viability of Matching
        for r in self.residents:
            if len(self.M[r]["assigned"]) > 1:
                return False

        for h in self.hospitals:
            capacity = self.hospitals[h]["capacity"]
            occupancy = len(self.M[h]["assigned"])
            if occupancy < capacity and self.been_full[h]:
                return False

        return True
