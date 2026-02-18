import random
import csv
from collections import defaultdict
import math
from Person_class import Person


class PersonFactory():
    def __init__(self):
        
        self.first_names = defaultdict(list)
        self.last_names = defaultdict(list)
        self.gender_prob = defaultdict(list)
        self.life_prob = {}
        self.birth_marriage = {}
        self.rank_prob = []
        
    def create_person(self,Elder_Age,Parent):
        #Desmond_Jones = Person(1950, Desmond_death, "Desmond", "Jones", None, None, Desmond_age)
        if not Parent and not Elder_Age:
            year_born = 1950
        elif Parent == None:
            year_born = Elder_Age +  random.randint(-5,5)
        else:
            year_born = math.ceil(Elder_Age) + random.randint(25,45) 
        #Make sure not past 2120
        if year_born > 2120:
            return None
        
        death = year_born + float(self.life_prob[str(year_born)])+ random.randint(-10,10) 
        decade_key = self.get_decade(year_born)
        gender = self.get_gender(decade_key)
        first_name = self.first_gen(decade_key,gender)
        random_last_name = self.get_random_last_name(decade_key)

        New_Child = Person(
            year_born,
            death,
            first_name,
            Parent.lastN if Parent else random_last_name,
            None,
            None,
            death-year_born,       
        )

        if Parent != None:
            Parent.children.append(New_Child)
        
        return New_Child
        
    def chance_kids(self,decade):
       
        marriage_chance =  float(self.birth_marriage[decade][1])
        is_married = random.choices(["marry", "single"], weights=[marriage_chance, 1-marriage_chance], k=1)[0]

        birth_rate = float(self.birth_marriage[decade][0])
        number_kids = math.ceil(birth_rate + random.uniform(-1.5,1.5))
        return number_kids, is_married
    
    def get_gender(self, decade):
        gender_vals = self.gender_prob[decade]
        
        genders = [item[0] for item in gender_vals]
        freq = [item[1] for item in gender_vals]
        
        gender = random.choices(genders, weights=freq, k=1)[0]
        return gender
        
    def get_decade(self,year):
        decade_int = (year // 10) * 10
        decade_key = str(decade_int) + "s"
        
        return decade_key
    
    def first_gen(self, decade,gender):
             
        gendered_options = [val for val in self.first_names[decade] if val[0] == gender]
   
        first_names = [val[1] for val in gendered_options]
        freq = [val[2] for val in gendered_options]

        name = random.choices(first_names, weights=freq, k=1)[0]
        return name
        
    def get_random_last_name(self,decade):
        last_names = self.last_names[decade]

        list_last_names = [item[1] for item in last_names]
      
        name = random.choices(list_last_names, weights=self.rank_prob, k=1)[0]
        return name
    
    def load_csv(self, filename):
        data = []
        with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            next(reader) # Skip header
            for row in reader:
                data.append(row)
        return data
    
    def get_files(self):   
        #create a map with {key=year: val=rest of the data}
        for rows in self.load_csv('birth_and_marriage_rates.csv'):
            self.birth_marriage[rows[0]] = (float(rows[1]), float(rows[2]))
            
        for rows in self.load_csv('first_names.csv'):
            self.first_names[rows[0]].append((rows[1],rows[2],float(rows[3])))
        
        for rows in self.load_csv('gender_name_probability.csv'):
            self.gender_prob[rows[0]].append((rows[1],float(rows[2])))
                                             
        for rows in self.load_csv('last_names.csv'):
            self.last_names[rows[0]].append((rows[1],rows[2]))
                                        
        for rows in self.load_csv('life_expectancy.csv'):
            self.life_prob[rows[0]] = (rows[1]) 

        with open('rank_to_probability.csv', mode='r') as infile:  
            reader = csv.reader(infile)
            row = next(reader)                                      
            for rows in row:
                self.rank_prob.append(float(rows))

