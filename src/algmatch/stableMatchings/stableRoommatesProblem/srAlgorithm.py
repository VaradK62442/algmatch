"""
Algorithm to produce a stable matching.
"""

from algmatch.stableMatchings.stableRoommatesProblem.srAbstract import SRAbstract


class SRAlgorithm(SRAbstract):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(filename=filename, dictionary=dictionary)

        self.unassigned_roommates = set()

        for roommate, r_prefs in self.men.items():
            if len(r_prefs["list"]) > 0:
                self.unassigned_roommates.add(roommate)
            self.M[roommate] = {"assigned": None}

    def _delete_pair(self, r_a, r_b):
        self.roommates[r_a]["list"].remove(r_b)
        self.roommates[r_b]["list"].remove(r_a)

        if len(self.roommates[r_a]["list"]) == 0:
            self.unassigned_roommates.discard(r_a)
        if len(self.roommates[r_b]["list"]) == 0:
            self.unassigned_roommates.discard(r_b)

    def _engage(self, r_a, r_b):
        self.M[r_a]["assigned"] = r_b
        self.M[r_b]["assigned"] = r_a

    def _free_up(self, r):
        self.M[r]["assigned"] = None
        if len(self.men[r]["list"]) > 0:
            self.unassigned_roommates.add(r)

    def phase_one(self):
        """
        Stable marriage-like proposal and refusal sequence
        """
        while self.unassigned_roommates:
            r_a = self.unassigned_roommates.pop()
            r_b = self.roommates[r_a]["list"][0]
            r_b_partner = self.M[r_b]["assigned"]

            if r_b_partner is not None:
                self._free_up(r_b_partner)
            self._engage(r_a, r_b)

            rank_r_a = self.roommate[r_b]["rank"][r_a]
            for reject in self.roommates[r_b]["list"][rank_r_a + 1 :]:
                self._delete_pair(reject, r_b)

    def phase_two(self):
        pass

    def _while_loop(self):
        self.phase_one()
        self.phase_two()

        for k, v in self.M.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    instance = {
        1: [4, 6, 2, 5, 3],
        2: [6, 3, 5, 1, 4],
        3: [4, 5, 1, 6, 2],
        4: [2, 6, 5, 1, 3],
        5: [4, 2, 3, 6, 1],
        6: [5, 1, 4, 2, 3],
    }
    SRAlgorithm(dictionary=instance)
