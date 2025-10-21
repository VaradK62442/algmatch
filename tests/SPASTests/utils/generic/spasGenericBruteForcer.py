class SPASGenericBruteForcer:
    def __init__(self):
        self.M = (
            {s: {"assigned": None} for s in self.students}
            | {p: {"assigned": set()} for p in self.projects}
            | {L: {"assigned": set()} for L in self.lecturers}
        )
        self.full_projects = set()
        self.full_lecturers = set()
        self.stable_matching_list = []

    def project_is_full(self, p):
        return self.projects[p]["capacity"] == len(self.M[p]["assigned"])

    def lecturer_is_full(self, L):
        return self.lecutrers[L]["capacity"] == len(self.M[L]["assigned"])

    def add_triple(self, student, project, lecturer):
        self.M[student] = project
        self.M[project].add(student)
        self.M[lecturer].add(student)

    def delete_triple(self, student, project, lecturer):
        self.M[student] = None
        self.M[project].remove(student)
        self.M[lecturer].remove(student)

    def save_matching(self):
        stable_matching = {"student_sided": {}, "lecturer_sided": {}}

        for student in self.students:
            assigned_project = self.M[student]["assigned"]
            if assigned_project is None:
                stable_matching["student_sided"][student] = ""
            else:
                stable_matching["student_sided"][student] = assigned_project

        for lecturer in self.lecturers:
            stable_matching["lecturer_sided"][lecturer] = self.M[lecturer][
                "assigned"
            ].copy()
        self.stable_matching_list.append(stable_matching)

    def has_stability(self) -> bool:
        # Link to problem description
        raise NotImplementedError("Enumerators need to link to a stability definition.")

    def student_trial_order(self, student) -> str:
        # generator for an order of projects in a student's preference list
        raise NotImplementedError("Enumerators need to describe the order of matching.")
