from algmatch.stableMatchings.stableMarriageProblem.smAbstract import SMAbstract

class MMSMS(SMAbstract):
    def __init__(self, dictionary):
        super(MMSMS, self).__init__(dictionary=dictionary)

        self.M = {m:{"assigned":None} for m in self.men} | {w:{"assigned":None} for w in self.women}
        self.assigned_men = set()
        self.assigned_women = set()
        self.minmax_matchings = []

    
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

    # ------------------------------------------------------------------------
    # The choose function finds all the matchings in the given instance
    # The check_stability function is used to print only the stable matchings
    # ------------------------------------------------------------------------
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
                if woman not in self.assigned_women:
                    self.M[man]["assigned"] = woman
                    self.M[woman]["assigned"] = man
                    self.assigned_women.add(woman)

                    self.man_choose(i+1)
                    if len(self.minmax_matchings) == 1:
                        return

                    self.M[man]["assigned"] = None
                    self.M[woman]["assigned"] = None
                    self.assigned_women.remove(woman)
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
                if man not in self.assigned_men:
                    self.M[woman]["assigned"] = man
                    self.M[man]["assigned"] = woman
                    self.assigned_men.add(man)

                    self.woman_choose(i+1)
                    if len(self.minmax_matchings) == 2:
                        return

                    self.M[woman]["assigned"] = None
                    self.M[man]["assigned"] = None
                    self.assigned_men.remove(man)
            # case where the woman is unassigned
            self.woman_choose(i+1)

    # alias with more readable name
    def find_minmax_matchings(self):
        self.man_choose()
        self.M = {m:{"assigned":None} for m in self.men} | {w:{"assigned":None} for w in self.women}
        self.woman_choose()