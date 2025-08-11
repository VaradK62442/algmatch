"""
Student Project Allocation With Ties - Abstact Class
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
        self.conditions_1b = (
            self._blockingpair_1bi_2bi,
            self._blockingpair_1bii,
            self._blockingpair_1biii,
        )
        self.conditions_2b = (
            self._blockingpair_1bi_2bi,
            self._blockingpair_2bii,
            self._blockingpair_2biii,
        )
        self.is_stable = False

    @staticmethod
    def _assert_valid_stability_type(st) -> None:
        assert st is not None, "Select a stability type - either 'super' or 'strong'"
        assert type(st) is str, "Stability type is not str'"
        assert st.lower() in ("super", "strong"), (
            "Stability type must be either 'super' or 'strong'"
        )

    def _blockingpair_1bi_2bi(self, _, project, lecturer):
        cj = self.projects[project]["upper_quota"]
        dk = self.original_lecturers[lecturer]["upper_quota"]

        project_occupancy = len(self.M[project]["assigned"])
        lecturer_occupancy = len(self.M[lecturer]["assigned"])

        if project_occupancy < cj and lecturer_occupancy < dk:
            return True
        return False

    def _blockingpair_1bii(self, student, project, lecturer):
        cj = self.projects[project]["upper_quota"]
        dk = self.original_lecturers[lecturer]["upper_quota"]

        project_occupancy = len(self.M[project]["assigned"])
        lecturer_occupancy = len(self.M[lecturer]["assigned"])

        if project_occupancy < cj and lecturer_occupancy == dk:
            Mlk_students = self.M[lecturer]["assigned"]
            lk_rankings = self.original_lecturers[lecturer]["rank"]

            if student in Mlk_students:
                return True

            student_rank = lk_rankings[student]
            for worst_student in Mlk_students:
                worst_student_rank = lk_rankings[worst_student]
                if student_rank <= worst_student_rank:
                    return True

        return False

    def _blockingpair_1biii(self, student, project, lecturer):
        cj = self.projects[project]["upper_quota"]
        project_occupancy = len(self.M[project]["assigned"])

        if project_occupancy == cj:
            lkj_rankings = self.lecturers[lecturer]["rank"]
            student_rank = lkj_rankings[student]
            for worst_student in self.M[project]["assigned"]:
                worst_student_rank = lkj_rankings[worst_student]
                if student_rank <= worst_student_rank:
                    return True
        return False

    def _blockingpair_2bii(self, student, project, lecturer):
        cj = self.projects[project]["upper_quota"]
        dk = self.original_lecturers[lecturer]["upper_quota"]

        project_occupancy = len(self.M[project]["assigned"])
        lecturer_occupancy = len(self.M[lecturer]["assigned"])

        if project_occupancy < cj and lecturer_occupancy == dk:
            Mlk_students = self.M[lecturer]["assigned"]
            lk_rankings = self.original_lecturers[lecturer]["rank"]

            if student in Mlk_students:
                return True

            student_rank = lk_rankings[student]
            for worst_student in Mlk_students:
                worst_student_rank = lk_rankings[worst_student]
                if student_rank < worst_student_rank:
                    return True

        return False

    def _blockingpair_2biii(self, student, project, lecturer):
        cj = self.projects[project]["upper_quota"]
        project_occupancy = len(self.M[project]["assigned"])

        if project_occupancy == cj:
            lkj_rankings = self.lecturers[lecturer]["rank"]
            student_rank = lkj_rankings[student]
            for worst_student in self.M[project]["assigned"]:
                worst_student_rank = lkj_rankings[worst_student]
                if student_rank < worst_student_rank:
                    return True
        return False

    def _check_super_stability(self) -> bool:
        raise NotImplementedError("Super-stability checking isn't implemented")

    def _check_strong_stability(self) -> bool:
        for student, s_prefs in self.original_students.items():
            preferred_projects = s_prefs["list"]
            indifferent_projects = []
            matched_project = self.M[student]["assigned"]

            if matched_project is not None:
                rank_matched_project = s_prefs["rank"][matched_project]
                preferred_projects = [
                    p for tie in s_prefs["list"][:rank_matched_project] for p in tie
                ]
                indifferent_projects = [
                    p for p in s_prefs["list"][rank_matched_project]
                ]
                indifferent_projects.remove(matched_project)

            for p_tie in preferred_projects:
                for project in p_tie:
                    lecturer = self.projects[project]["lecturer"]
                    for condition in self.conditions_1b:
                        if condition(student, project, lecturer):
                            return False

            for p_tie in indifferent_projects:
                for project in p_tie:
                    lecturer = self.projects[project]["lecturer"]
                    for condition in self.conditions_2b:
                        if condition(student, project, lecturer):
                            return False
        return True

    def _while_loop(self):
        raise NotImplementedError("Method _while_loop must be implemented in subclass")

    def run(self) -> None:
        self._while_loop()

        for student in self.students:
            project = self.M[student]["assigned"]
            if project is not None:
                lecturer = self.projects[project]["lecturer"]
                self.stable_matching["student_sided"][student] = project
                self.stable_matching["lecturer_sided"][lecturer].append(student)

            if self.stability_type == "super":
                self.is_stable = self._check_super_stability()
            else:
                self.is_stable = self._check_strong_stability()

            if self.is_stable:
                return f"stable matching: {self.stable_matching}"
        return "no stable matching"
