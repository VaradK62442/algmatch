from algmatch.stableMatchings.stableMarriageProblem.smAbstract import SMAbstract

class MMSMS(SMAbstract):
    def __init__(self, dictionary):
        SMAbstract.__init__(self,dictionary=dictionary)

        self.M = {}
        self.minmax_matchings = []

    def setup_M(self):
        self.M.clear()
        self.M.update({m:{"assigned":None} for m in self.men})
        self.M.update({w:{"assigned":None} for w in self.women})

    def save_matching(self):
        stable_matching = {"man_sided":{},"woman_sided":{}}
        for man in self.men:
            if self.M[man]["assigned"] is None:
                stable_matching["man_sided"][man] = ''
            else:
                stable_matching["man_sided"][man] = self.M[man]["assigned"]
        for woman in self.women:
            if self.M[woman]["assigned"] is None:
                stable_matching["woman_sided"][woman] = ''
            else:
                stable_matching["woman_sided"][woman] = self.M[woman]["assigned"]
        self.minmax_matchings.append(stable_matching)

    def add_pair(self, man, woman):
        self.M[man]["assigned"] = woman
        self.M[woman]["assigned"] = man

    def delete_pair(self, man, woman):
        self.M[man]["assigned"] = None
        self.M[woman]["assigned"] = None
    
    def man_choose(self, i=1):
        #if every man is assigned
        if i > len(self.men):
            #if stable add to solutions list
            if self._check_stability():
                self.save_matching()

        else:
            man = 'm'+str(i)
            for woman in self.men[man]["list"]:
                # avoid the multiple assignment of women
                if self.M[woman]["assigned"] is None:
                    self.add_pair(man, woman)

                    self.man_choose(i+1)
                    # found, now exit
                    if len(self.minmax_matchings) == 1:
                        return

                    self.delete_pair(man, woman)
            # case where the man is unassigned
            self.man_choose(i+1)

    def woman_choose(self, i=1):
        #if every woman is assigned
        if i > len(self.women):
            #if stable add to solutions list
            if self._check_stability():
                self.save_matching()

        else:
            woman = 'w'+str(i)
            for man in self.women[woman]["list"]:
                # avoid the multiple assignment of men
                if self.M[man]["assigned"] is None:
                    self.add_pair(man, woman)

                    self.woman_choose(i+1)
                    if len(self.minmax_matchings) == 2:
                        return

                    self.delete_pair(man, woman)
            # case where the woman is unassigned
            self.woman_choose(i+1)

    def find_minmax_matchings(self):
        self.setup_M()
        self.man_choose()

        self.setup_M()
        self.woman_choose()