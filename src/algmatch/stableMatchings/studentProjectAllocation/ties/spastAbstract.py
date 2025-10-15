"""
Student Project Allocation With Lecturer Preferences Over Students
- With Ties
- Abstract class
"""

from copy import deepcopy
import os

from algmatch.stableMatchings.studentProjectAllocation.ties.spastPreferenceInstance import (
    SPASTPreferenceInstance,
)


class SPASTAbstract:
    def __init__(
        self,
        filename: str | None = None,
        dictionary: dict | None = None,
        stability_type: str = None,
    ) -> None:
        assert filename is not None or dictionary is not None, (
            "Either filename or dictionary must be provided"
        )
        assert not (filename is not None and dictionary is not None), (
            "Only one of filename or dictionary must be provided"
        )

        self._assert_valid_stability_type(stability_type)
        self.stability_type = stability_type.lower()

        if filename is not None:
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._reader = SPASTPreferenceInstance(filename=filename)

        if dictionary is not None:
            self._reader = SPASTPreferenceInstance(dictionary=dictionary)

        self.students = self._reader.students
        self.projects = self._reader.projects
        self.lecturers = self._reader.lecturers

        # we need original copies of the preference lists to check the stability of solutions
        self.original_students = deepcopy(self.students)
        self.original_lecturers = deepcopy(self.lecturers)

        self.M = {}  # provisional matching
        self.stable_matching = {
            "student_sided": {student: "" for student in self.students},
            "lecturer_sided": {lecturer: [] for lecturer in self.lecturers},
        }

        self.super_blocking_conditions = (
            self._blocking_pair_bi,
            self._blocking_pair_bii,
            self._blocking_pair_biii,
        )
        self.is_stable = False

    @staticmethod
    def _assert_valid_stability_type(st) -> None:
        assert st is not None, "Select a stability type - either 'super' or 'strong'"
        assert type(st) is str, "Stability type is not str'"
        assert st.lower() in ("super", "strong"), (
            "Stability type must be either 'super' or 'strong'"
        )

    def _get_lecturer_worst_existing_student(self, lecturer):
        existing_students = self.M[lecturer]["assigned"]

        if len(existing_students) == 0:
            return None

        def rank_comparator(x):
            return -self.lecturers[lecturer]["rank"][x]

        return min(existing_students, key=rank_comparator)

    def _get_project_worst_existing_student(self, project):
        existing_students = self.M[project]["assigned"]

        if len(existing_students) == 0:
            return None

        def rank_comparator(x):
            return -self.projects[project]["rank"][x]

        return min(existing_students, key=rank_comparator)

    def _blocking_pair_bi(self, _, project, lecturer):
        cj = self.projects[project]["capacity"]
        dk = self.original_lecturers[lecturer]["capacity"]

        project_occupancy = len(self.M[project]["assigned"])
        lecturer_occupancy = len(self.M[lecturer]["assigned"])

        if project_occupancy < cj and lecturer_occupancy < dk:
            return True
        return False

    def _blocking_pair_bii(self, student, project, lecturer):
        cj = self.projects[project]["capacity"]
        dk = self.original_lecturers[lecturer]["capacity"]

        project_occupancy = len(self.M[project]["assigned"])
        lecturer_occupancy = len(self.M[lecturer]["assigned"])

        if project_occupancy < cj and lecturer_occupancy == dk:
            Mlk_students = self.M[lecturer]["assigned"]
            if student in Mlk_students:  # s_i \in M(lk)
                return True

            lk_rankings = self.original_lecturers[lecturer]["rank"]
            student_rank = lk_rankings[student]
            worst_student = self._get_lecturer_worst_existing_student(lecturer)
            worst_student_rank = lk_rankings[worst_student]
            if student_rank <= worst_student_rank:
                return True
        return False

    def _blocking_pair_biii(self, student, project, _):
        cj = self.projects[project]["capacity"]
        project_occupancy = len(self.M[project]["assigned"])

        if project_occupancy == cj:
            lkj_rankings = self.projects[project]["rank"]
            student_rank = lkj_rankings[student]
            worst_student = self._get_project_worst_existing_student(project)
            worst_student_rank = lkj_rankings[worst_student]
            if student_rank <= worst_student_rank:
                return True
        return False

    def _check_super_stability(self) -> bool:
        # stability must be checked with regards to the original lists prior to deletions
        for student, s_prefs in self.original_students.items():
            # catch multiple assignments
            assignment_num = len(self.M[student]["assigned"])
            if assignment_num > 1:
                return False
            elif assignment_num == 1:
                [matched_project] = self.M[student]["assigned"]
            else:
                matched_project = None

            if matched_project is None:
                preferred_projects = s_prefs["list"]
            else:
                rank_matched_project = s_prefs["rank"][matched_project]
                # every project that s_i prefers to her matched project
                # or is indifferent between them
                preferred_projects = s_prefs["list"][:rank_matched_project]

            for p_tie in preferred_projects:
                for project in p_tie:
                    if project == matched_project:
                        continue

                    lecturer = self.projects[project]["lecturer"]
                    for condition in self.super_blocking_conditions:
                        if condition(student, project, lecturer):
                            return False

        return True

    def _check_strong_stability(self) -> bool:
        raise NotImplementedError(
            "Strong stability algorithms have not yet been published for SPAST"
        )

    def _while_loop(self) -> bool:
        raise NotImplementedError("Method _while_loop must be implemented in subclass")

    def _save_student_sided(self) -> None:
        for student in self.students:
            project_set = self.M[student]["assigned"]
            if project_set != set():
                # If student is multiply assigned then there's no stable matching,
                # in which case we won't call this function, so we can use this unpacking
                [project] = project_set
                self.stable_matching["student_sided"][student] = project

    def _save_lecturer_sided(self) -> None:
        for lecturer in self.lecturer:
            student_set = self.M[lecturer]["assigned"]
            if student_set != set():
                self.stable_matching["lecturer_sided"][lecturer] = student_set

    def run(self) -> None:
        if self._while_loop():
            self._save_student_sided()
            self._save_lecturer_sided()

            if self.stability_type == "super":
                self.is_stable = self._check_super_stability()
            else:
                self.is_stable = self._check_strong_stability()

            if self.is_stable:
                return f"super-stable matching: {self.stable_matching}"
        return "no super-stable matching"
