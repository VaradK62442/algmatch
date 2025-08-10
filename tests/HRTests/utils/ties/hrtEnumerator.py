from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtAbstract import (
    HRTAbstract,
)
from tests.HRTests.utils.generic.hrGenericEnumerator import HRGenericEnumerator


class HRTEnumerator(HRTAbstract, HRGenericEnumerator):
    def __init__(self, dictionary, stability_type):
        HRTAbstract.__init__(self, dictionary=dictionary, stability_type=stability_type)
        HRGenericEnumerator.__init__(self)

    def has_stability(self) -> bool:
        for person in self.M:
            assignee = self.M[person]["assigned"]
            if assignee is None:
                self.M[person]["assigned"] = set()
            elif isinstance(assignee, str):
                self.M[person]["assigned"] = set([assignee])

        if self.stability_type == "super":
            return self._check_super_stability()
        elif self.stability_type == "strong":
            return self._check_strong_stability()
        else:
            raise ValueError("Stability type is neither 'super' or 'strong'")

    def resident_trial_order(self, resident):
        for tie in self.residents[resident]["list"]:
            for hospital in tie:
                yield hospital
