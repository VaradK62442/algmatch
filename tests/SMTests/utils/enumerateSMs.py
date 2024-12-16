from algmatch.stableMatchings.stableMarriageProblem.smAbstract import SMAbstract

class ESMS(SMAbstract):
    def __init__(self, dictionary):
        SMAbstract.__init__(self,dictionary=dictionary)

        self.M = {m:{"assigned":None} for m in self.men} | {w:{"assigned":None} for w in self.women}
        self.all_stable_matchings = []

    
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
        self.all_stable_matchings.append(stable_matching)

    def add_pair(self, man, woman):
        self.M[man]["assigned"] = woman
        self.M[woman]["assigned"] = man

    def delete_pair(self, man, woman):
        self.M[man]["assigned"] = None
        self.M[woman]["assigned"] = None
        
    def choose(self, i=1):
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
                    self.choose(i+1)
                    self.delete_pair(man, woman)
            # case where the man is unassigned
            self.choose(i+1)

    # alis with more readable name
    def find_all_stable_matchings(self):
        self.choose()