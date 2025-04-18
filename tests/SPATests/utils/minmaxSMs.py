from algmatch.stableMatchings.studentProjectAllocation.noTies.spaAbstract import SPAAbstract


class MMSMS(SPAAbstract):
    def __init__(self, dictionary):
        super(MMSMS, self).__init__(dictionary=dictionary)

        self.M = {}
        self.minmax_matchings = []

        # This lets us order students in the stable matching by number.
        # We cannot use 'sorted' without this key because that uses lexial order.
        self.student_order_comparator = lambda s: int(s[1:])

    def setup_M(self):
        self.M.update({s: {"assigned": None} for s in self.students})
        self.M.update({p: {"assigned": set()} for p in self.projects})
        self.M.update({L: {"assigned": set()} for L in self.lecturers})

    def project_is_overfull(self, p):
        return self.projects[p]["upper_quota"] < len(self.M[p]["assigned"])

    def lecturer_is_overfull(self, L):
        return self.lecturers[L]["upper_quota"] < len(self.M[L]["assigned"])

    def add_triple(self, student, project, lecturer):
        self.M[student]["assigned"] = project
        self.M[project]["assigned"].add(student)
        self.M[lecturer]["assigned"].add(student)

    def delete_triple(self, student, project, lecturer):
        self.M[student]["assigned"] = None
        self.M[project]["assigned"].remove(student)
        self.M[lecturer]["assigned"].remove(student)

    def save_matching(self):
        stable_matching = {"student_sided": {}, "lecturer_sided": {}}
        for student in self.students:
            if self.M[student]["assigned"] is None:
                stable_matching["student_sided"][student] = ""
            else:
                stable_matching["student_sided"][student] = self.M[student]["assigned"]
        for lecturer in self.lecturers:
            stable_matching["lecturer_sided"][lecturer] = sorted(
                self.M[lecturer]["assigned"], key=self.student_order_comparator
            )
        self.minmax_matchings.append(stable_matching)

    # ------------------------------------------------------------------------
    # The choose function finds all the matchings in the given instance
    # The inherited _check_stability function is used to print only the stable matchings
    # ------------------------------------------------------------------------
    def student_choose(self, i=1):
        # if every resident is assigned
        if i > len(self.students):
            for project in self.projects:
                if self.project_is_overfull(project):
                    return
            for lecturer in self.lecturers:
                if self.lecturer_is_overfull(lecturer):
                    return
            # if stable add to solutions list
            if self._check_stability():
                self.save_matching()

        else:
            student = f"s{i}"
            for project in self.students[student]["list"]:
                lecturer = self.projects[project]["lecturer"]
                self.add_triple(student, project, lecturer)

                self.student_choose(i + 1)
                if len(self.minmax_matchings) == 1:
                    return

                self.delete_triple(student, project, lecturer)
            # case where the student is unassigned
            self.student_choose(i + 1)

    def project_choose(self, i=1):
        # if every resident is assigned
        if i > len(self.projects):
            for project in self.projects:
                if self.project_is_overfull(project):
                    return
            for lecturer in self.lecturers:
                if self.lecturer_is_overfull(lecturer):
                    return
            # if stable add to solutions list
            if self._check_stability():
                self.save_matching()

        else:
            project = f"p{i}"
            lecturer = self.projects[project]["lecturer"]
            for student in self.projects[project]["list"]:
                self.add_triple(student, project, lecturer)

                self.student_choose(i + 1)
                if len(self.minmax_matchings) == 2:
                    return

                self.delete_triple(student, project, lecturer)
            # case where the student is unassigned
            self.project_choose(i + 1)

    # alias with more readable name
    def find_minmax_matchings(self):
        self.setup_M()
        self.student_choose()

        self.setup_M()
        self.project_choose()
