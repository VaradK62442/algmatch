import random

from tests.abstractTestClasses.abstractInstanceGenerator import AbstractInstanceGenerator

class SMInstanceGenerator(AbstractInstanceGenerator):
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

        self.instance = {"men" : {}, "women" : {}}

        # lists of numbers that will be shuffled to get preferences
        self.available_men = [i+1 for i in range(self.no_men)]
        self.available_women = [i+1 for i in range(self.no_women)]

        
    def generate_instance_no_ties(self):
        # ====== RESET INSTANCE ======
        self.instance = {"men" : {i+1 : [] for i in range(self.no_men)},
                         "women" : {i+1 : [] for i in range(self.no_women)}}

        # ====== MEN ====== 
        for man_list in self.instance["men"].values():
            length = random.randint(self.li, self.lj)
            # we provide this many preferred women at random
            random.shuffle(self.available_women)
            man_list.extend(self.available_women[:length])

        # ====== WOMEN ======
        for woman_list in self.instance["women"].values():
            length = random.randint(self.li, self.lj) 
            #  we provide this many preferred men at random
            random.shuffle(self.available_men)
            woman_list.extend(self.available_men[:length])

        return self.instance