import random

from tests.HRTests.utils.generic.hrGenericGenerator import HRGenericGenerator


class HRTInstanceGenerator(HRGenericGenerator):
    def __init__(self, residents, hospitals, lower_bound, upper_bound):
        super().__init__(residents, hospitals, lower_bound, upper_bound)
        self.tie_density = 0  # default to none

    def set_tie_density(self, tie_density):
        assert tie_density >= 0 and tie_density <= 1, "Tie density must be in [0,1]."
        self.tie_density = tie_density

    def _generate_residents_lists(self):
        for res_list in self.instance["residents"].values():
            random.shuffle(self.available_hospitals)

            length = random.randint(self.li, self.lj)
            res_list.append([self.available_hospitals[0]])
            for hospital in self.available_hospitals[1:length]:
                if random.uniform(0, 1) < self.tie_density:
                    res_list[-1].append(hospital)
                else:
                    res_list.append([hospital])

    def _generate_hospitals_lists(self):
        for hos_dict in self.instance["residents"].values():
            random.shuffle(self.available_hospitals)

            hos_dict["capacity"] = random.randint(1, self.no_residents)

            hos_list = hos_dict["preferences"]
            hos_list.append([self.available_hospitals[0]])
            for resident in self.available_residents:
                if random.uniform(0, 1) < self.tie_density:
                    hos_list[-1].append(resident)
                else:
                    hos_list.append([resident])
