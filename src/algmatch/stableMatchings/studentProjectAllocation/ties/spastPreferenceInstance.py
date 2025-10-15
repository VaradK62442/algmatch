"""
Store preference lists for the SPAST stable matching algorithm.
"""

from itertools import product

from algmatch.abstractClasses.abstractPreferenceInstanceWithTies import (
    AbstractPreferenceInstanceWithTies,
)
from algmatch.stableMatchings.studentProjectAllocation.ties.fileReader import FileReader
from algmatch.stableMatchings.studentProjectAllocation.ties.dictionaryReader import (
    DictionaryReader,
)


class SPASTPreferenceInstance(AbstractPreferenceInstanceWithTies):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(filename, dictionary)
        self._setup_project_lists()
        self._general_setup_procedure()

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

    def _setup_project_lists(self) -> None:
        for project in self.projects:
            lec = self.projects[project]["lecturer"]
            self.lecturers[lec]["projects"].add(project)
            lecturer_list = self.lecturers[lec]["list"]
            self.projects[project]["list"] = lecturer_list[:]

    def check_preference_lists(self) -> None:
        self.check_preferences_with_ties_single_group(
            self.students, "student", self.projects
        )
        self.check_preferences_with_ties_single_group(
            self.lecturers, "lecturer", self.students
        )

    def clean_unacceptable_pairs(self) -> None:
        for s, p in product(self.students, self.projects):
            s_list = self.students[s]["list"]
            p_list = self.projects[p]["list"]

            s_found = any([s in tie for tie in p_list])
            p_found = any([p in tie for tie in s_list])

            if not (s_found and p_found):
                for tie in s_list:
                    tie.discard(p)
                for tie in p_list:
                    tie.discard(s)
                # clean empty sets
                # we've produced at most one per side in this loop
                if set() in s_list:
                    s_list.remove(set())
                if set() in p_list:
                    p_list.remove(set())

        for L in self.lecturers:
            proj_pref_set = set()
            for p in self.lecturers[L]["projects"]:
                for tie in self.projects[p]["list"]:
                    proj_pref_set.update(tie)
            new_l_prefs = []
            for s_tie in self.lecturers[L]["list"]:
                new_tie = s_tie & proj_pref_set
                new_l_prefs.append(new_tie)
            self.lecturers[L]["list"] = new_l_prefs

    def set_up_rankings(self):
        self.tied_lists_to_rank(self.students)
        self.tied_lists_to_rank(self.projects)
        self.tied_lists_to_rank(self.lecturers)
