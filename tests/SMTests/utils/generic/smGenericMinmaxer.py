from tests.SMTests.utils.generic.smGenericBruteForcer import SMGenericBruteForcer


class SMGenericMinmaxer(SMGenericBruteForcer):
    def __init__(self):
        SMGenericBruteForcer.__init__(self)

    def man_choose(self, i=1):
        # if every man is assigned
        if i > len(self.men):
            # if stable add to solutions list
            if self.has_stability():
                self.save_matching()

        else:
            man = "m" + str(i)
            for woman in self.man_trial_order(man):
                # avoid the multiple assignment of women
                if self.M[woman]["assigned"] is None:
                    self.add_pair(man, woman)

                    self.man_choose(i + 1)
                    # found, now exit
                    if len(self.stable_matching_list) == 1:
                        return

                    self.delete_pair(man, woman)
            # case where the man is unassigned
            self.man_choose(i + 1)

    def woman_choose(self, i=1):
        # if every woman is assigned
        if i > len(self.women):
            # if stable add to solutions list
            if self.has_stability():
                self.save_matching()

        else:
            woman = "w" + str(i)
            for man in self.woman_trial_order(woman):
                # avoid the multiple assignment of men
                if self.M[man]["assigned"] is None:
                    self.add_pair(man, woman)

                    self.woman_choose(i + 1)
                    if len(self.stable_matching_list) == 2:
                        return

                    self.delete_pair(man, woman)
            # case where the woman is unassigned
            self.woman_choose(i + 1)

    def setup_M(self):
        self.M.clear()
        self.M.update({m: {"assigned": None} for m in self.men})
        self.M.update({w: {"assigned": None} for w in self.women})

    def find_stable_matchings(self):
        self.setup_M()
        self.man_choose()

        self.setup_M()
        self.woman_choose()
