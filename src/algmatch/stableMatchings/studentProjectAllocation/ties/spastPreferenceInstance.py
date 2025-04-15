"""
Store preference lists for student project allocation with ties algorithm.
"""

from itertools import product

from algmatch.abstractClasses.abstractPreferenceInstance import (
    AbstractPreferenceInstance,
)
from algmatch.stableMatchings.studentProjectAllocation.ties.fileReader import FileReader
from algmatch.stableMatchings.studentProjectAllocation.ties.dictionaryReader import (
    DictionaryReader,
)
from algmatch.stableMatchings.studentProjectAllocation.ties.entityPreferenceInstance import (
    EntityPreferenceInstance as EPI,
)

from algmatch.errors.InstanceSetupErrors import PrefRepError, PrefNotFoundError


class SPASTPreferenceInstance(AbstractPreferenceInstance):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(filename, dictionary)
        self.setup_project_lists()

    def _load_from_file(self, filename: str) -> None:
        reader = FileReader(filename)
        self.students = reader.students
        self.projects = reader.projects
        self.lecturers = reader.lecturers

    def _load_from_dictionary(self, dictionary: dict) -> None:
        reader = DictionaryReader(dictionary)
        self.students = reader.students
        self.projects = reader.projects
        self.lecturers = reader.lecturers

    def setup_project_lists(self) -> None:
        for project in self.projects:
            lec = self.projects[project]["lecturer"]
            self.lecturers[lec]["projects"].add(project)
            lecturer_list = self.lecturers[lec]["list"]

            project_list = []
            for epi in lecturer_list:
                if epi.isTie:
                    project_list.append([])
                    for stu in epi.values:
                        for elt in self.students[stu.values]["list"]:
                            if project in elt:
                                project_list[-1].append(str(stu.values))
                                #print(f"appended {stu.values} (tie)")

                else:
                    for elt in self.students[epi.values]["list"]:
                        if project in elt:
                            project_list.append(str(epi.values))
                            #print(f"appended {epi.values} (no tie)")

            self.lecturers[lec]["lkj"][project] = [
                EPI(tuple(p)) if isinstance(p, list) else EPI(p)
                for p in project_list
                if p != []
            ]

    # TODO: check these work
    # unused currently
    def check_preference_lists(self) -> None:
        for s, s_prefs in self.students.items():
            if len(set(s_prefs["list"])) != len(s_prefs["list"]):
                raise PrefRepError("student", s)

            for p in s_prefs["list"]:
                if p not in self.projects:
                    raise PrefNotFoundError("student", s, p)

        for L, L_prefs in self.lecturers.items():
            if len(set(L_prefs["list"])) != len(L_prefs["list"]):
                raise PrefRepError("lecturer", L)

            for s in L_prefs["list"]:
                if s not in self.students:
                    raise PrefNotFoundError("lecturer", L, s)

    def clean_unacceptable_pairs(self) -> None:
        for s, p in product(self.students, self.projects):
            if s not in self.projects[p]["list"] or p not in self.students[s]["list"]:
                try:
                    self.students[s]["list"].remove(p)
                except ValueError:
                    pass
                try:
                    self.projects[p]["list"].remove(s)
                except ValueError:
                    pass

        for L in self.lecturers:
            proj_pref_set = set()
            for p in self.lecturers[L]["projects"]:
                proj_pref_set.update(self.projects[p]["list"])
            new_l_prefs = []
            for s in self.lecturers[L]["list"]:
                if s in proj_pref_set:
                    new_l_prefs.append(s)
            self.lecturers[L]["list"] = new_l_prefs

    def set_up_rankings(self):
        for s in self.students:
            self.students[s]["rank"] = {
                project: idx for idx, project in enumerate(self.students[s]["list"])
            }
        for p in self.projects:
            self.projects[p]["rank"] = {
                student: idx for idx, student in enumerate(self.projects[p]["list"])
            }
        for L in self.lecturers:
            self.lecturers[L]["rank"] = {
                student: idx for idx, student in enumerate(self.lecturers[L]["list"])
            }
