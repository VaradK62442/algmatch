from tests.HRTests.utils.generic.hrGenericBruteForcer import HRGenericBruteForcer


class HRGenericMinmaxer(HRGenericBruteForcer):
    def __init__(self):
        HRGenericBruteForcer.__init__(self)

    def resident_choose(self, i=1):
        # if every resident is assigned
        if i > len(self.residents):
            # if stable add to solutions list
            if self.has_stability():
                self.save_matching()

        else:
            resident = "r" + str(i)
            for hospital in self.resident_trial_order(resident):
                # avoid the over-filling of hospitals
                if hospital not in self.full_hospitals:
                    self.add_pair(resident, hospital)
                    if self.hospital_is_full(hospital):
                        self.full_hospitals.add(hospital)

                    self.resident_choose(i + 1)
                    if len(self.stable_matching_list) == 1:
                        return

                    self.delete_pair(resident, hospital)
                    self.full_hospitals.discard(hospital)
            # case where the resident is unassigned
            self.resident_choose(i + 1)

    def hospital_choose(self, i=1):
        # if every resident is assigned
        if i > len(self.hospitals):
            # if stable add to solutions list
            if self.has_stability():
                print("hos found")
                self.save_matching()

        else:
            hospital = "h" + str(i)
            for resident in self.hospital_trial_order(hospital):
                # avoid the over-filling of hospitals
                if self.M[resident]["assigned"] is None:
                    self.add_pair(resident, hospital)

                    self.hospital_choose(i + 1)
                    if len(self.stable_matching_list) == 2:
                        return

                    self.delete_pair(resident, hospital)
            # case where the hospital is empty
            self.hospital_choose(i + 1)

    def setup_M(self):
        self.M.clear()
        self.M.update({r: {"assigned": None} for r in self.residents})
        self.M.update({h: {"assigned": set()} for h in self.hospitals})

    def find_stable_matchings(self):
        self.setup_M()
        self.resident_choose()

        self.setup_M()
        self.hospital_choose()
