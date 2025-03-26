"""
Store preference lists for student project allocation algorithm.
"""

from algmatch.abstractClasses.abstractPreferenceInstance import (
    AbstractPreferenceInstance,
)
from algmatch.stableMatchings.studentProjectAllocation.noTies.fileReader import (
    FileReader,
)
from algmatch.stableMatchings.studentProjectAllocation.noTies.dictionaryReader import (
    DictionaryReader,
)


class SPAPreferenceInstance(AbstractPreferenceInstance):
    def __init__(
        self, filename: str | None = None, dictionary: dict | None = None
    ) -> None:
        super().__init__(filename, dictionary)
        self.setup_project_lists()
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

    def setup_project_lists(self) -> None:
        for project in self.projects:
            lec = self.projects[project]["lecturer"]
            self.lecturers[lec]["projects"].add(project)
            lecturer_list = self.lecturers[lec]["list"]
            self.projects[project]["list"] = lecturer_list[:]

    def check_preference_lists(self) -> None:
        self.check_preferences_single_group(self.students, "student", self.projects)
        self.check_preferences_single_group(self.lecturers, "lecturer", self.students)

    def clean_unacceptable_pairs(self) -> None:
        super().clean_unacceptable_pairs(self.students, self.projects)

        for L in self.lecturers:
            proj_pref_set = set()
            for p in self.lecturers[L]["projects"]:
                proj_pref_set.update(self.projects[p]["list"])
            new_l_prefs = []
            for s in self.lecturers[L]["list"]:
                if s in proj_pref_set:
                    new_l_prefs.append(s)
            self.lecturers[L]["list"] = new_l_prefs

    def set_up_rankings(self) -> None:
        self.tieless_lists_to_rank(self.students)
        self.tieless_lists_to_rank(self.projects)
        self.tieless_lists_to_rank(self.lecturers)
