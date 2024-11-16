"""
Class to read in a dictionary of preferences for the Student Project Allocation stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader


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
                        preferences = [f"p{i}" for i in v]
                        rank = {proj: idx for idx, proj in enumerate(preferences)}

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
                        preferences = [f"s{i}" for i in v["preferences"]]
                        rank = {stud: idx for idx, stud in enumerate(preferences)}

                        self.lecturers[lecturer] = {"upper_quota": capacity, "projects": set(), "list": preferences, "rank": rank}

        for project in self.projects:
            lec = self.projects[project]["lecturer"]
            self.lecturers[lec]["projects"].add(project)
            lecturer_list = self.lecturers[lec]["list"]
            project_list = [stu for stu in lecturer_list if project in self.students[stu]["list"]]
            rank = {stud: idx for idx, stud in enumerate(project_list)}
            self.projects[project]["list"] = project_list
            self.projects[project]["rank"] = rank