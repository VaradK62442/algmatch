from algmatch.stableMatchings.studentProjectAllocation.spaAbstract import SPAAbstract

class ESMS(SPAAbstract):
    def __init__(self, filename):
        super(ESMS, self).__init__(filename=filename)

        self.M.update({s:{"assigned":None} for s in self.students})
        self.M.update({p:{"assigned":set()} for p in self.projects})
        self.M.update({L:{"assigned":set()} for L in self.lecturers})

        self.all_stable_matchings = []

        # This lets us order residents in the stable matching by number.
        # We cannot use 'sorted' without this key because that uses lexial order.
        self.student_order_comparator = lambda s: int(s[1:])

    def project_is_overfull(self, p):
        return self.projects[p]["upper_quota"] < len(self.M[p]["assigned"])
    
    def lecturer_is_overfull(self, L):
        return self.lecturers[L]["upper_quota"] < len(self.M[L]["assigned"])
    
    def save_matching(self):
        stable_matching = {"student_sided":{},"lecturer_sided":{}}
        for student in self.students:
            if self.M[student]["assigned"] is None:
                stable_matching["student_sided"][student] = ''
            else:
                stable_matching["student_sided"][student] = self.M[student]["assigned"]
        for lecturer in self.lecturers:
            stable_matching["lecturer_sided"][lecturer] = sorted(self.M[lecturer]["assigned"], key=self.student_order_comparator)
        self.all_stable_matchings.append(stable_matching)

    # ------------------------------------------------------------------------
    # The choose function finds all the matchings in the given instance
    # The inherited _check_stability function is used to print only the stable matchings
    # ------------------------------------------------------------------------
    def choose(self, i=1):
        #if every resident is assigned
        if i > len(self.students):
            for project in self.projects:
                if self.project_is_overfull(project):
                    return
            for lecturer in self.lecturers:
                if self.lecturer_is_overfull(lecturer):
                    return
            #if stable add to solutions list
            if self._check_stability():
                self.save_matching()

        else:
            student = f"s{i}"
            for project in self.students[student]["list"]:
                lecturer = self.projects[project]["lecturer"]

                self.M[student]["assigned"] = project
                self.M[project]["assigned"].add(student)
                self.M[lecturer]["assigned"].add(student)

                self.choose(i+1)

                self.M[student]["assigned"] = None
                self.M[project]["assigned"].remove(student)
                self.M[lecturer]["assigned"].remove(student)
            # case where the student is unassigned
            self.choose(i+1)

    # alias with more readable name
    def find_all_stable_matchings(self):
        self.choose()