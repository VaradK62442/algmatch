"""
Class to read in a dictionary of preferences for the Student Project Allocation with Ties stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.stableMatchings.studentProjectAllocation.ties.entityPreferenceInstance import EntityPreferenceInstance

class DictionaryReader(AbstractReader):
    def __init__(self, dictionary: dict) -> None:
        super().__init__(dictionary)
        self._read_data()

    def _read_data(self) -> None:
        self.students = {}
        self.projects = {}
        self.lecturers = {}

        for key, value in self.data.items():
            match key:
                case "students":
                    for k, v in value.items():
                        student = f"s{k}"
                        preferences = []
                        rank = {}
                        for i, elt in enumerate(v):
                            if isinstance(elt, int):
                                epi = EntityPreferenceInstance(f"p{elt}")
                                rank[f"p{elt}"] = i
                            else:
                                epi = EntityPreferenceInstance(tuple(f"p{j}" for j in elt))
                                for j in elt:
                                    rank[f"p{j}"] = i

                            preferences.append(epi)

                        self.students[student] = {"list": preferences, "rank": rank}

                case "projects":
                    for k, v in value.items():
                        project = f"p{k}"
                        capacity = v["capacity"]
                        lecturer = f"l{v['lecturer']}"

                        self.projects[project] = {"upper_quota": capacity, "lecturer": lecturer}

                case "lecturers":
                    for k, v in value.items():
                        lecturer = f"l{k}"
                        capacity = v["capacity"]

                        preferences = []
                        rank = {}

                        for i, elt in enumerate(v["preferences"]):
                            if isinstance(elt, int):
                                epi = EntityPreferenceInstance(f"s{elt}")
                                rank[f"s{elt}"] = i
                            else:
                                epi = EntityPreferenceInstance(tuple(f"s{j}" for j in elt))
                                for j in elt:
                                    rank[f"s{j}"] = i

                            preferences.append(epi)

                        self.lecturers[lecturer] = {"upper_quota": capacity, "projects": set(), "list": preferences, "rank": rank}

        for project in self.projects:
            lec = self.projects[project]["lecturer"]
            self.lecturers[lec]["projects"].add(project)
            lecturer_list = self.lecturers[lec]["list"]

            # TODO: beautify?
            project_list = []
            for epi in lecturer_list:
                if epi.isTie:
                    for stu in epi.values:
                        for elt in self.students[stu.values]["list"]:
                            if project in elt:
                                project_list.append(stu.values)
                
                else:
                    for elt in self.students[epi.values]["list"]:
                        if project in elt:
                            project_list.append(epi.values)

            rank = {stud: idx for idx, stud in enumerate(project_list)}
            self.projects[project]["list"] = project_list
            self.projects[project]["rank"] = rank