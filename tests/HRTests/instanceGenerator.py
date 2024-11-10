import random

class HR:
    def __init__(self, residents, hospitals, lower_bound, upper_bound):
        if residents <= 0 or type(residents) != int:
            raise ValueError("number of residents must be a postive integer")
        if hospitals <= 0 or type(hospitals) != int:
            raise ValueError("number of men must be a postive integer")
        if type(lower_bound) != int or type(upper_bound) != int:
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
        # ====== RESIDENTS ======= 
        self.residents = {i+1 : {"list": []} for i in range(self.no_residents)}
        for res in self.residents:
            length = random.randint(self.li, self.lj)
            # we provide this many preferred women at random
            random.shuffle(self.available_hospitals)
            self.residents[res]["list"] = self.available_hospitals[:length]

        # ====== HOSPITALS ======= 
        self.hospitals = {i+1 : {"capacity": 0, "list": []} for i in range(self.no_hospitals)}
        for hos in self.hospitals:
            # random capacity; 1 <= capacity <= residents
            self.hospitals[hos]["capacity"] = random.randint(1,self.no_residents)
            # we provide a random ordering of all residents
            random.shuffle(self.available_residents)
            self.hospitals[hos]["list"] = self.available_residents[:]

    def write_instance_no_ties(self, filename):  # writes to txt file
        if type(filename) != str:
            raise ValueError("Filename is not a string.")

        with open(filename, 'w') as I:

            # write the numbers of residents and hospitals as the header
            I.write(str(self.no_residents)+' '+str(self.no_hospitals)+'\n')
            
            # write indexes, capacities and preferences, 
            # see the DATA_FORMAT_GUIDELINE.md in src/stableMachings/hospitalResidentsProblem
            for n in range(1, self.no_residents + 1):
                preferences = self.residents[n]["list"]
                I.write(str(n) + ' ' + ' '.join([str(h) for h in preferences]) + '\n')

            for n in range(1, self.no_hospitals + 1):
                capacity = self.hospitals[n]["capacity"]
                preferences = self.hospitals[n]["list"]
                I.write(str(n) + ' ' + str(capacity) + ' ' +' '.join([str(r) for r in preferences]) + '\n')

            I.close()