"""
Hospital/Residents Problem With Ties - Strong-Stability-Specific Abstract Class
Stores implementations of:
- Gabow's algorithm for maximum matching
- Finding the critical set of residents based on the above
- Definition of domination
"""

from collections import deque
from copy import deepcopy

from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtAbstract import (
    HRTAbstract,
)


class HRTStrongAbstract(HRTAbstract):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(
            filename=filename, dictionary=dictionary, stability_type="strong"
        )
        # used to find the critical set and final answer
        self.maximum_matching = {}
        self.dist = {}
        self.G_r = {}

    def _reset_G_r(self):
        self.G_r = deepcopy(self.M)
        for hospital, h_info in self.hospitals.items():
            self.G_r[hospital]["quota"] = h_info["capacity"]

    def _reset_maximum_matching(self):
        self.maximum_matching = {
            "resident": {r: None for r in self.residents},
            "hospital": {h: set() for h in self.hospitals},
        }
        self.dist = {}

    def _remove_from_G_r(self, resident):
        for hospital in self.G_r[resident]["assigned"].copy():
            self.G_r[resident]["assigned"].remove(hospital)
            self.G_r[hospital]["assigned"].remove(resident)

    def _form_G_r(self):
        self._reset_G_r()

        bound_residents = set()
        for h in self.hospitals:
            capacity = self.hospitals[h]["capacity"]
            occupancy = len(self.M[h]["assigned"])
            if occupancy <= capacity:
                for r in self.G_r[h]["assigned"].copy():
                    bound_residents.add(r)
                    self.G_r[h]["quota"] -= 1

            else:
                h_tail = self._get_tail(h)
                for r in self.G_r[h]["assigned"] - h_tail:
                    bound_residents.add(r)
                    self.G_r[h]["quota"] -= 1

        for r in bound_residents:
            self._remove_from_G_r(r)

    def _get_maximum_matching_in_G_r(self):
        """
        An implementation of Gabow 1983.
        """
        raise NotImplementedError()

    def _select_maximum_matching_in_G_r(self):
        raise NotImplementedError()

    def _get_critical_set(self):
        raise NotImplementedError()

    def _get_domination_index(self, hospital):
        capacity = self.hospitals[hospital]["capacity"]
        seen_residents = 0
        for idx, r_tie in enumerate(self._get_pref_list(hospital)):
            seen_residents += len(r_tie & self.M[hospital]["assigned"])
            if seen_residents >= capacity:
                return idx
        raise ValueError(f"Hospital {hospital} was not full or oversubscribed.")

    def _delete_dominated_residents(self, hospital):
        dom_idx = self._get_domination_index(hospital)
        for reject_tie in self._get_pref_list(hospital)[dom_idx + 1 :]:
            for reject in reject_tie.copy():
                self._break_assignment(hospital, reject)
                self._delete_pair(hospital, reject)
