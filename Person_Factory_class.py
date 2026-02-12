import pandas as pd
import random
import csv
from collections import defaultdict
import math
from Person_class import Person


class PersonFactory():
    def __init__(self):
        
        #Desmond_Jones = Person(1950,61, "Desmond", "Jones", None, None)
        #Molly_Jones = Person(1950,61, "Molly", "Jones", None, None) 
        #Desmond_Jones.partner = Molly_Jones
        #Molly_Jones.partner = Desmond_Jones
        #self.Tree = create_family_tree()
        
        self.firstNames = defaultdict(list)
        self.lastNames = defaultdict(list)
        self.genderProb = defaultdict(list)
        self.lifeProb = {}
        self.birth_marriage = {}
        self.familyTree = None
        
    def create_family_tree(self):
        #initial death
        Molly_death = 1950 + float(self.lifeProb["1950"]) + random.randint(-10,10)
        Desmond_death = 1950 + float(self.lifeProb["1950"]) + random.randint(-10,10)
        
        #intial Ages
        Molly_age = Molly_death - 1950
        Desmond_age = Desmond_death - 1950
        
        Desmond_Jones = Person(
            1950,
            Desmond_death,
            "Desmond", 
            "Jones", 
            None,
            None, 
            Desmond_age
        )
        Molly_Jones = Person(
            1950,
            Molly_death,
            "Molly",
            "Jones",
            None,
            None,
            Molly_age
        ) 
        
        #initial Partner assignment
        Desmond_Jones.partner = Molly_Jones
        Molly_Jones.partner = Desmond_Jones
        
        #initial Children 
        if Molly_Jones.age >= Desmond_Jones.age:
            
            year = Molly_Jones.year_born
            decade_key = self.get_decade(year)
            print(decade_key)
            
            number_kids = self.chance_kids(decade_key)
            print(number_kids)

            for i in range(number_kids):
                self.createChildren(Molly_Jones.age,Molly_Jones)
        else:
            year = Desmond_Jones.year_born
            decade_key = self.get_decade(year)
            print(decade_key)
            
            number_kids = self.chance_kids(decade_key)
            print(number_kids)

            for i in range(number_kids):
                self.createChildren(Desmond_Jones.age,Desmond_Jones)
                
           

          
    def createChildren(self,Elder_Age,Parent):
        #Desmond_Jones = Person(1950, Desmond_death, "Desmond", "Jones", None, None, Desmond_age)
        year_born = Parent.year_born + random.randint(25,45)
        death = float(self.lifeProb[str(year_born)]) + random.randint(-10,10)
        
        decade_key = self.get_decade(year_born)
        
        gender = self.get_gender(decade_key)
        first_name = self.first_gen(decade_key,gender)
        
        New_Child = Person(
            year_born,
            death,
            #Need to create random name logic
            first_name,
            Parent.lastN,
            None,
            None,
            death-year_born,       
        )
        Parent.children.append(New_Child)
        
    def chance_kids(self,decade):
        birth_rate = float(self.birth_marriage[decade][0])

        number_kids = math.ceil(birth_rate + random.uniform(-1.5,1.5))
        return number_kids
    
    def get_gender(self, decade):
        gender_vals = self.genderProb[decade]
        
        
        genders = [item[0] for item in gender_vals] # ['male', 'female']
        freq = [item[1] for item in gender_vals]
        
        gender = random.choices(genders, weights=freq, k=1)[0]
        return gender
        
    def get_decade(self,year):
        decade_int = (year // 10) * 10
        decade_key = str(decade_int) + "s"
        
        return decade_key
    
    def first_gen(self, decade,gender):
        
        decade_values = []
        
        gendered_options = [val for val in self.firstNames[decade] if val[0] == gender]
   
        first_names = [val[1] for val in gendered_options]

    
        freq = [val[2] for val in gendered_options]


        name = random.choices(first_names, weights=freq, k=1)[0]
        return name
        
        
    
    def get_files(self):
        
        #create a map with {key=year: val= (birth,marriage)}
        with open('birth_and_marriage_rates.csv', mode='r') as infile:
            reader = csv.reader(infile)
            #skip header
            next(reader)
            for rows in reader:
                self.birth_marriage[rows[0]] = (float(rows[1]), float(rows[2]))
                
        
        with open('first_names.csv', mode='r') as infile:
            reader = csv.reader(infile)
            #skip header
            next(reader)
            for rows in reader:
                self.firstNames[rows[0]].append((rows[1],rows[2],float(rows[3])))
                
        with open('gender_name_probability.csv', mode='r') as infile:
            reader = csv.reader(infile)
            #skip header
            next(reader)
            for rows in reader:
                self.genderProb[rows[0]].append((rows[1],float(rows[2])))
                                            
        with open('last_names.csv', mode='r') as infile:
            reader = csv.reader(infile)
            #skip header
            next(reader)
            for rows in reader:
                self.lastNames[rows[0]].append((rows[1],rows[2]))
                
                                            
        with open('life_expectancy.csv', mode='r') as infile:
            reader = csv.reader(infile)
            #skip header
            next(reader)
            for rows in reader:
                self.lifeProb[rows[0]] = (rows[1]) 
                
        
        
    def print(self):
        print(self.familyTree)
    
        

