"""
Class to read in file for a SPA-P instance.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        
        self.students = {} # student -> [project preferences, {project: assigned?}]
        self.projects = {} # project -> [capacity, lecturer, num students assigned]
        self.lecturers = {} # lecturer -> [capacity, project preferences, num students assigned, worst project]
        
        self._read_data()


    def _read_data(self) -> None:
        with open (self.data, 'r') as f:
            f = f.readlines()
            student_size, project_size, _ = map(int, f[0].strip().split())

            for l in f[1:student_size+1]:
                line = l.strip().split()
                self.students[f's{line[0]}'] = [
                    [f'p{i}' for i in line[1:]],
                    {f'p{i}': 0 for i in line[1:]}
                ]

            for l in f[student_size+1:student_size+project_size+1]:
                line = l.strip().split()
                self.projects[f'p{line[0]}'] = [
                    int(line[1]),
                    f'l{line[2]}',
                    0
                ]

            for l in f[student_size+project_size+1:]:
                line = l.strip().split()
                self.lecturers[f'l{line[0]}'] = [
                    int(line[1]),
                    [f'p{i}' for i in line[2:]],
                    0,
                    None
                ]