import random

class SMInstanceGenerator:
    def __init__(self, men, women, lower_bound, upper_bound):
        if men <= 0 or type(men) is not int:
            raise ValueError("number of men must be a postive integer")
        if women <= 0 or type(women) is not int:
            raise ValueError("number of men must be a postive integer")
        if type(lower_bound) is not int or type(upper_bound) is not int:
            raise ValueError("Bound must be integers.")
        if lower_bound < 0:
            raise ValueError("Lower bound is negative.")
        if upper_bound > min(men, women):
            raise ValueError("Upper bound is greater than the number of men or the number of women.")
        if lower_bound > upper_bound:
            raise ValueError("Lower bound is greater than upper bound")

        self.no_men = men
        self.no_women = women
        self.li = lower_bound
        self.lj = upper_bound 

        self.men = {} # man dictionary
        self.women = {} # woman dictionary

        # lists of numbers that will be shuffled to get preferences
        self.available_men = [i+1 for i in range(self.no_men)]
        self.available_women = [i+1 for i in range(self.no_women)]

        
    def generate_instance_no_ties(self):
        # ====== MEN ======= 
        self.men = {i+1 : {"list": []} for i in range(self.no_men)}
        for man in self.men:
            length = random.randint(self.li, self.lj)
            # we provide this many preferred women at random
            random.shuffle(self.available_women)
            self.men[man]["list"] = self.available_women[:length]

        # ====== WOMEN ======= 
        self.women = {i+1 : {"list": []} for i in range(self.no_women)}
        for woman in self.women:
            length = random.randint(self.li, self.lj) 
            #  we provide this many preferred men at random
            random.shuffle(self.available_men)
            self.women[woman]["list"] = self.available_men[:length]

    def write_instance_no_ties(self, filename):  # writes to txt file
        if type(filename) is not str:
            raise ValueError("Filename is not a string.")

        with open(filename, 'w') as Instance:

            # write the numbers of men and women as the header
            Instance.write(str(self.no_men)+' '+str(self.no_women)+'\n')
            
            # write indexes and preferences, see the DATA_FORMAT_GUIDELINE.md in src/stableMachings/stableMarriageProblem
            for n in range(1, self.no_men + 1):
                preferences = self.men[n]["list"]
                Instance.write(str(n) + ' ' + ' '.join([str(w) for w in preferences]) + '\n')

            for n in range(1, self.no_women + 1):
                preferences = self.women[n]["list"]
                Instance.write(str(n) + ' ' + ' '.join([str(m) for m in preferences]) + '\n')

            Instance.close()