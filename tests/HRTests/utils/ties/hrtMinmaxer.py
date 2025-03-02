from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtAbstract import (
    HRTAbstract,
)
from tests.HRTests.utils.generic.hrGenericMinmaxer import HRGenericMinmaxer


class HRMinmaxer(HRTAbstract, HRGenericMinmaxer):
    def __init__(self, dictionary):
        HRTAbstract.__init__(self, dictionary=dictionary)
        HRGenericMinmaxer.__init__(self)

    def has_stability(self) -> bool:
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

    def hospital_trial_order(self, hospital):
        for tie in self.hopsitals[hospital]["list"]:
            for resident in tie:
                yield resident
