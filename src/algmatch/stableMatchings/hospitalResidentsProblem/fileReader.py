"""
Class to read in a file of preferences for the Hospitals/Residents Problem stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.abstractClasses.abstractReader import ReaderError

class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_residents = 0
        self.no_hospitals = 0
        self.residents = {}                
        self.hospitals = {}
        cur_line = 1
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        try:
            self.no_residents, self.no_hospitals = map(int, file[0].split())
        except ValueError:
            raise ReaderError(f"line {cur_line}", "Participant Quantities Misformatted")

        # build residents dictionary
        for elt in file[1:self.no_residents+1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise ReaderError(f"line {cur_line}", "Resident ID misformatted")
            resident = f"r{entry[0]}"
            if resident in self.residents:
                raise ReaderError(f"line {cur_line}", "Repeated resident ID")

            for i in entry[1:]:
                if not i.isdigit():
                    raise ReaderError(f"line {cur_line}", "Resident preference list misformatted; {i} is not int>0")
            preferences = [f"h{i}" for i in entry[1:]]

            self.residents[resident] = {"list": preferences, "rank": {}}

        # build hospitals dictionary
        for elt in file[self.no_residents+1:self.no_residents+self.no_hospitals+1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise ReaderError(f"line {cur_line}", "Hospital ID misformatted")
            hospital = f"h{entry[0]}"
            if hospital in self.hospitals:
                raise ReaderError(f"line {cur_line}", "Repeated hospital ID")

            capacity = int(entry[1])
            preferences = [f"r{i}" for i in entry[2:]]

            self.hospitals[hospital] = {"capacity": capacity, "list": preferences, "rank": {}}