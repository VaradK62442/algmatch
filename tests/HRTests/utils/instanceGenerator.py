import random

from tests.abstractTestClasses.abstractInstanceGenerator import AbstractInstanceGenerator

class HRInstanceGenerator(AbstractInstanceGenerator):
    def __init__(self, residents, hospitals, lower_bound, upper_bound):
        if residents <= 0 or type(residents) is not int:
            raise ValueError("number of residents must be a postive integer")
        if hospitals <= 0 or type(hospitals) is not int:
            raise ValueError("number of men must be a postive integer")
        if type(lower_bound) is not int or type(upper_bound) is not int:
            raise ValueError("Bound must be integers.")
        if lower_bound < 0:
            raise ValueError("Lower bound is negative.")
        if upper_bound > hospitals:
            raise ValueError("Upper bound is greater than the number of hospitals.")
        if lower_bound > upper_bound:
            raise ValueError("Lower bound is greater than upper bound")

        self.no_residents = residents
        self.no_hospitals = hospitals
        self.li = lower_bound
        self.lj = upper_bound 

        self.residents = {}
        self.hospitals = {}
        
        # lists of numbers that will be shuffled to get preferences
        self.available_residents = [i+1 for i in range(self.no_residents)]
        self.available_hospitals = [i+1 for i in range(self.no_hospitals)]

    def generate_instance_no_ties(self):
        # ====== RESET INSTANCE ======
        self.instance = {"residents" : {i+1 : [] for i in range(self.no_residents)},
                         "hospitals" : {i+1 : {"capacity":0,"preferences":[]} for i in range(self.no_hospitals)}}

        # ====== RESIDENTS ======= 
        for res_list in self.instance["residents"].values():
            length = random.randint(self.li, self.lj)
            # we provide this many preferred hospitals at random
            random.shuffle(self.available_hospitals)
            res_list.extend(self.available_hospitals[:length])

        # ====== HOSPITALS ======= 
        for hos_dict in self.instance["hospitals"].values():
            # random capacity; 1 <= capacity <= residents
            hos_dict["capacity"] = random.randint(1,self.no_residents)
            # we provide a random ordering of all residents
            random.shuffle(self.available_residents)
            hos_dict["list"] = self.available_residents[:]


        return self.instance