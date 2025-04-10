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
            self._blockingpair_1bi,
            self._blockingpair_1bii,
            self._blockingpair_1biii,
        )
        self.conditions_2b = (
            self._blockingpair_2bi,
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

    def blockingpair_1bi(self, _, project, lecturer):
        if self.plc[project][1] > 0 and self.lp[lecturer][0] > 0:
            return True
        return False

    def blockingpair_1bii(self, student, project, lecturer):
        if self.plc[project][1] > 0 and self.lp[lecturer][0] == 0:
            proj_in_M = self.M[student]
            if proj_in_M != "" and self.plc[proj_in_M][0] == lecturer:
                return True
            lec_worst_pointer = self.lecturer_wstcounter[lecturer][0]
            student_rank_Lk = self.lp_rank[lecturer][student]
            if student_rank_Lk <= lec_worst_pointer:
                return True
        return False

    def blockingpair_1biii(self, student, project, _):
        if self.plc[project][1] == 0:
            proj_worst_pointer = self.project_wstcounter[project][0]
            student_rank_Lkj = self.proj_rank[project][student]
            if student_rank_Lkj <= proj_worst_pointer:
                return True
        return False

    def blockingpair_2bi(self, _, project, lecturer):
        if self.plc[project][1] > 0 and self.lp[lecturer][0] > 0:
            return True
        return False

    def blockingpair_2bii(self, student, project, lecturer):
        if self.plc[project][1] > 0 and self.lp[lecturer][0] == 0:
            proj_in_M = self.M[student]
            if proj_in_M != "" and self.plc[proj_in_M][0] == lecturer:
                return True
            lec_worst_pointer = self.lecturer_wstcounter[lecturer][0]
            student_rank_Lk = self.lp_rank[lecturer][student]
            if student_rank_Lk < lec_worst_pointer:
                return True
        return False

    def blockingpair_2biii(self, student, project, _):
        if self.plc[project][1] == 0:
            proj_worst_pointer = self.project_wstcounter[project][0]
            student_rank_Lkj = self.proj_rank[project][student]
            if student_rank_Lkj < proj_worst_pointer:
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

            for project in preferred_projects:
                lecturer = self.plc[project][0]
                for condition in self.conditions_1b:
                    if condition(student, project, lecturer):
                        return False

            for project in indifferent_projects:
                lecturer = self.plc[project][0]
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
