from algmatch.stableMatchings.hospitalResidentsProblem.noTies.hrAbstract import (
    HRAbstract,
)
from tests.HRTests.utils.generic.hrGenericMinmaxer import HRGenericMinmaxer


class HRMinmaxer(HRAbstract, HRGenericMinmaxer):
    def __init__(self, dictionary):
        HRAbstract.__init__(self, dictionary=dictionary)
        HRGenericMinmaxer.__init__(self)

    def has_stability(self):
        return self._check_stability()

    def resident_trial_order(self, resident):
        for hospital in self.residents[resident]["list"]:
            yield hospital

    def hospital_trial_order(self, hospital):
        for resident in self.hospitals[hospital]["list"]:
            yield resident
