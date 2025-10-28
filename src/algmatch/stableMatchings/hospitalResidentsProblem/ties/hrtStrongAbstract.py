"""
Hospital/Residents Problem With Ties - Strong-Stability-Specific Abstract Class
Stores implementations of:
- Gabow's algorithm for maximum matching
- Finding the critical set of residents based on the above
"""

from collections import deque

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

    def _reset_maximum_matching(self):
        self.maximum_matching = {
            "resident": {r: None for r in self.residents},
            "hospital": {h: set() for h in self.hospitals},
        }
        self.dist = {}

    def _get_maximum_matching(self):
        raise NotImplementedError()

    def _select_maximum_matching(self):
        self._get_maximum_matching()
        for m, w in self.maximum_matching["men"].items():
            self.M[m]["assigned"] = w
        for w, m in self.maximum_matching["women"].items():
            self.M[w]["assigned"] = m
