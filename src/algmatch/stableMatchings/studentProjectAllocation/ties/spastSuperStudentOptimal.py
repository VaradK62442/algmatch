"""
Algorithm to produce M_0, the student-optimal, lecturer-pessimal super-stable matching, where such a thing exists.
"""

from algmatch.stableMatchings.studentProjectAllocation.ties.spastAbstract import (
    SPASTAbstract,
)


class SPASTSuperStudentOptimal(SPASTAbstract):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(
            filename=filename, dictionary=dictionary, stability_type="super"
        )

        self.unassigned_students = set()
        self.been_full = {p: False for p in self.projects}

        for student, s_prefs in self.students.items():
            if len(s_prefs["list"]) > 0:
                self.unassigned_students.add(student)
            self.M[student] = {"assigned": set()}

        for project in self.projects:
            self.M[project] = {"assigned": set()}

        for lecturer in self.lecturers:
            self.M[lecturer] = {"assigned": set()}

    def _delete_triple(self, student, project, lecturer):
        super()._delete_triple(student, project, lecturer)
        if self._get_pref_length(student) == 0:
            self.unassigned_students.discard(student)

    def _break_assignment(self, student, project, lecturer):
        super()._break_assignment(student, project, lecturer)
        if self._get_pref_length(student) > 0:
            self.unassigned_students.add(student)

    def _while_loop(self) -> bool:
        while len(self.unassigned_students) != 0:
            while len(self.unassigned_students) != 0:
                s = self.unassigned_students.pop()
                p_tie = self._get_head(s)
                for p in p_tie.copy():
                    L = self.projects[p]["lecturer"]
                    self._assign(s, p, L)

                    p_capacity = self.projects[p]["capacity"]
                    p_occupancy = len(self.M[p]["assigned"])
                    if p_occupancy > p_capacity:
                        self._delete_tail_project(p)
                    else:
                        l_capacity = self.lecturers[L]["capacity"]
                        l_occupancy = len(self.M[L]["assigned"])
                        if l_occupancy > l_capacity:
                            self._delete_tail_lecturer(L)

                    p_capacity = self.projects[p]["capacity"]
                    p_occupancy = len(self.M[p]["assigned"])
                    l_capacity = self.lecturers[L]["capacity"]
                    l_occupancy = len(self.M[L]["assigned"])
                    if p_occupancy == p_capacity:
                        self.been_full[p] = True
                        s_worst = self._get_project_worst_existing_student(p)
                        self._reject_project_lower_ranks(s_worst, p, L)
                    if l_occupancy == l_capacity:
                        s_worst = self._get_lecturer_worst_existing_student(L)
                        self._reject_lecturer_lower_ranks(s_worst, L)

            for p in self.projects:
                if not self.been_full[p]:
                    continue
                p_info = self.projects[p]

                p_capacity = p_info["capacity"]
                p_occupancy = len(self.M[p]["assigned"])
                if p_occupancy < p_capacity:
                    L = p_info["lecturer"]
                    sr = p_info["best_reject"]
                    self._reject_lecturer_lower_ranks(sr, L)

        # placeholding for simpler stability conditions
        return self._check_super_stability()
