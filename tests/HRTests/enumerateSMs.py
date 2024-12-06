from algmatch.stableMatchings.hospitalResidentsProblem.hrAbstract import HRAbstract

class ESMS(HRAbstract):
    def __init__(self, dictionary):
        super(ESMS, self).__init__(dictionary=dictionary)

        self.M = {r:{"assigned":None} for r in self.residents} | {h:{"assigned":set()} for h in self.hospitals}
        self.full_hospitals = set()
        self.all_stable_matchings = []

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
        self.all_stable_matchings.append(stable_matching)

    def add_pair(self, resident, hospital):
        self.M[resident]["assigned"] = hospital
        self.M[hospital]["assigned"].add(resident)

        if self.hospital_is_full(hospital):
            self.full_hospitals.add(hospital)
            
    def delete_pair(self, resident, hospital):
        self.M[resident]["assigned"] = None
        self.M[hospital]["assigned"].remove(resident)
        self.full_hospitals.discard(hospital)
    
    def choose(self, i=1):
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
                    self.choose(i+1)
                    self.delete_pair(resident, hospital)
            # case where the resident is unassigned
            self.choose(i+1)

    # alias with more readable name
    def find_all_stable_matchings(self):
        self.choose()