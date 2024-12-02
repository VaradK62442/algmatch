"""
Class to read in a file of preferences for the Stable Marriage Problem stable matching algorithm.
"""
from re import findall

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.errors.ReaderErrors import (
    IDMisformatError,
    NestedTiesError,
    ParticipantQuantityError,
    RepeatIDError,
    UnclosedTieError,
    UnopenedTieError
)

class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def regex_split(self,line):
        return findall(r"\d+|[\(\)]", line)

    def _scan_preference_tokens(self,token_list,gender,pref_char):
        preferences = []
        in_tie = False
        cur_set = set()
        for token in token_list[1:]:
            if token == '(':
                if in_tie:
                    raise NestedTiesError(gender, self.cur_line)
                in_tie = True
            elif token == ')':
                if not in_tie:
                    raise UnopenedTieError(gender, self.cur_line)
                in_tie = False
                preferences.append(cur_set.copy())
                cur_set.clear()
            else:
                cur_set.add(pref_char+token)
                if not in_tie:
                    preferences.append(cur_set.copy())
                    cur_set.clear()
        if in_tie:
            raise UnclosedTieError(gender, self.cur_line)
        return preferences

    def _read_data(self) -> None:
        self.no_men = 0
        self.no_women = 0
        self.men = {}                
        self.women = {}
        self.cur_line = 1
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        try:
            self.no_men, self.no_women = map(int, file[0].split())
        except ValueError:
            raise ParticipantQuantityError()

        # build men dictionary
        for elt in file[1:self.no_men+1]:
            self.cur_line += 1
            entry = self.regex_split(elt)

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("man", self.cur_line, line=True)
            man = f"m{entry[0]}"
            if man in self.men:
                raise RepeatIDError("man", self.cur_line, line=True)
            
            # we don't check that every token is a digit
            # this became unnecessary with the use of re.findall

            preferences = self._scan_preference_tokens(entry,"man","w")
            self.men[man] = {"list": preferences, "rank": {}}

        # build women dictionary
        for elt in file[self.no_men+1:self.no_men+self.no_women+1]:
            self.cur_line += 1
            entry = self.regex_split(elt)

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("woman",self.cur_line,line=True)
            woman = f"w{entry[0]}"
            if woman in self.women:
                raise RepeatIDError("woman",self.cur_line,line=True)

            preferences = self._scan_preference_tokens(entry,"woman","m")
            self.women[woman] = {"list": preferences, "rank": {}}