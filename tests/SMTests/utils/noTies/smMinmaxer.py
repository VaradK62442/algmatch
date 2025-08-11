from algmatch.stableMatchings.stableMarriageProblem.noTies.smAbstract import SMAbstract
from tests.SMTests.utils.generic.smGenericMinmaxer import SMGenericMinmaxer


class SMMinmaxer(SMAbstract, SMGenericMinmaxer):
    def __init__(self, dictionary):
        SMAbstract.__init__(self, dictionary=dictionary)
        SMGenericMinmaxer.__init__(self)

    def has_stability(self) -> bool:
        return self._check_stability()

    def man_trial_order(self, man):
        for woman in self.men[man]["list"]:
            yield woman

    def woman_trial_order(self, woman):
        for man in self.women[woman]["list"]:
            yield man
