import random

from tests.SMTests.utils.generic.smGenericGenerator import SMGenericGenerator


class SMTInstanceGenerator:
    def __init__(self, men, women, lower_bound, upper_bound):
        SMGenericGenerator.__init__(self, men, women, lower_bound, upper_bound)

    def generate_instance(self, tie_density):
        assert tie_density >= 0 and tie_density <= 1, "Tie density must be in [0,1]."
        self._reset_instance()
        self._generate_men_lists(tie_density)
        self._generate_women_lists(tie_density)
        return self.instance

    def _generate_men_lists(self, tie_density):
        for man_list in self.instance["men"].values():
            random.shuffle(self.available_women)

            length = random.randint(self.li, self.lj)
            man_list = [[self.available_women[0]]]
            for woman in self.available_women[:length]:
                if random.uniform(0, 1) < tie_density:
                    man_list[-1].append(woman)
                else:
                    man_list.append([woman])

    def _generate_women_lists(self, tie_density):
        for woman_list in self.instance["women"].values():
            random.shuffle(self.available_men)

            length = random.randint(self.li, self.lj)
            woman_list = [[self.available_men[0]]]
            for man in self.available_men[:length]:
                if random.uniform(0, 1) < tie_density:
                    woman_list[-1].append(man)
                else:
                    woman_list.append([man])
