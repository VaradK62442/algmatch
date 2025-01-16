from algmatch.stableMatchings.hospitalResidentsProblem.hrAbstract import HRAbstract

class MMSMS(HRAbstract):
    def __init__(self, dictionary):
        super(MMSMS, self).__init__(dictionary=dictionary)

        self.M = {}
        self.full_hospitals = set()
        self.minmax_matchings = []

        # This lets us order residents in the stable matching by number.
        # We cannot use 'sorted' without this key because that uses lexial order.
        self.resident_order_comparator = lambda r: int(r[1:])

    def setup_M(self):
        self.M.clear()
        self.M.update({r:{"assigned":None} for r in self.residents})
        self.M.update({h:{"assigned":set()} for h in self.hospitals})

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

    def add_pair(self, resident, hospital):
        self.M[resident]["assigned"] = hospital
        self.M[hospital]["assigned"].add(resident)
            
    def delete_pair(self, resident, hospital):
        self.M[resident]["assigned"] = None
        self.M[hospital]["assigned"].remove(resident)
    
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
                    self.add_pair(resident, hospital)
                    if self.hospital_is_full(hospital):
                        self.full_hospitals.add(hospital)

                    self.resident_choose(i+1)
                    if len(self.minmax_matchings) == 1:
                        return

                    self.delete_pair(resident, hospital)
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
                if self.M["resident"] is not None:
                    self.add_pair(resident, hospital)

                    self.hospital_choose(i+1)
                    if len(self.minmax_matchings) == 2:
                        return

                    self.delete_pair(resident, hospital)
            # case where the resident is unassigned
            self.resident_choose(i+1)
    
    def find_minmax_matchings(self):
        self.setup_M()
        self.resident_choose()

        self.setup_M()
        self.hospital_choose()