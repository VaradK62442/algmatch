from algmatch.stableMatchings.hospitalResidentsProblem.hrAbstract import HRAbstract

class MMSMS(HRAbstract):
    def __init__(self, dictionary):
        super(MMSMS, self).__init__(dictionary=dictionary)

        self.M = {r:{"assigned":None} for r in self.residents} | {h:{"assigned":set()} for h in self.hospitals}
        self.assigned_residents = set()
        self.full_hospitals = set()
        self.minmax_matchings = []

        # This lets us order residents in the stable matching by number.
        # We cannot use 'sorted' without this key because that uses lexial order.
        self.resident_order_comparator = lambda r: int(r[1:])

    def hospital_is_full(self, h):
        return self.hospitals[h]["capacity"] == len(self.M[h]["assigned"])
    
    def save_matching(self):
        stable_matching = {"resident_sided":{},"hospital_sided":{}}
        for resident in self.residents:
            if self.M[resident]["assigned"] is None:
                stable_matching["resident_sided"][resident] = ''
            else:
                stable_matching["resident_sided"][resident] = self.M[resident]["assigned"]
        for hospital in self.hospitals:
            stable_matching["hospital_sided"][hospital] = sorted(self.M[hospital]["assigned"], key=self.resident_order_comparator)
        self.minmax_matchings.append(stable_matching)

    # ------------------------------------------------------------------------
    # The choose function finds all the matchings in the given instance
    # The inherited _check_stability function is used to print only the stable matchings
    # ------------------------------------------------------------------------
    def resident_choose(self, i=1):
        #if every resident is assigned
        if i > len(self.residents):
            #if stable add to solutions list
            if self._check_stability():
                self.save_matching()

        else:
            resident = 'r'+str(i)
            for hospital in self.residents[resident]["list"]:
                # avoid the over-filling of hospitals
                if hospital not in self.full_hospitals:
                    self.M[resident]["assigned"] = hospital
                    self.M[hospital]["assigned"].add(resident)

                    if self.hospital_is_full(hospital):
                        self.full_hospitals.add(hospital)

                    self.resident_choose(i+1)
                    if len(self.minmax_matchings) == 1:
                        return

                    self.M[resident]["assigned"] = None
                    self.M[hospital]["assigned"].remove(resident)
                    self.full_hospitals.discard(hospital)
            # case where the resident is unassigned
            self.resident_choose(i+1)

    def hospital_choose(self, i=1):
        #if every resident is assigned
        if i > len(self.hospitals):
            #if stable add to solutions list
            if self._check_stability():
                self.save_matching()

        else:
            hospital= 'h'+str(i)
            for resident in self.hospitals[hospital]["list"]:
                # avoid the over-filling of hospitals
                if resident not in self.assigned_residents:
                    self.M[resident]["assigned"] = hospital
                    self.M[hospital]["assigned"].add(resident)
                    self.assigned_residents.add(resident)

                    self.hospital_choose(i+1)
                    if len(self.minmax_matchings) == 2:
                        return

                    self.M[resident]["assigned"] = None
                    self.M[hospital]["assigned"].remove(resident)
                    self.assigned_residents.discard(resident)
            # case where the resident is unassigned
            self.resident_choose(i+1)
    
    # alias with more readable name
    def find_minmax_matchings(self):
        # resident optimal
        self.resident_choose()
        # reset
        self.M = {r:{"assigned":None} for r in self.residents} | {h:{"assigned":set()} for h in self.hospitals}
        # resident pessimal
        self.hospital_choose()