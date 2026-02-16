import pandas as pd
import random
import csv
from collections import defaultdict, deque
import math
from Person_class import Person


class PersonFactory():
    def __init__(self):
        
        self.firstNames = defaultdict(list)
        self.lastNames = defaultdict(list)
        self.genderProb = defaultdict(list)
        self.lifeProb = {}
        self.birth_marriage = {}
        self.familyTree = None
        
    def create_family_tree(self):
        #initial death
        #TODO: make death calculation into function
        Molly_death = 1950 + float(self.lifeProb["1950"]) + random.randint(-10,10)
        Desmond_death = 1950 + float(self.lifeProb["1950"]) + random.randint(-10,10)
        
        
        #intial Ages
        #TODO: make age calculation into function 
        Molly_age = Molly_death - 1950
        Desmond_age = Desmond_death - 1950
   
    
        Desmond_Jones = self.createChildren(None,None)
        Desmond_Jones.firstN = "Desmond"
        Desmond_Jones.lastN = "Jones"
   
        Molly_Jones = self.createChildren(None,None)
        Molly_Jones.firstN = "Molly"
        Molly_Jones.lastN = "Jones"
        self.familyTree = Desmond_Jones
        #initial Partner assignment
        Desmond_Jones.partner = Molly_Jones
        Molly_Jones.partner = Desmond_Jones
        
        #initial Children 
        year = Molly_Jones.year_born
        decade_key = self.get_decade(year)
        print(decade_key)
        
        number_kids,_ = self.chance_kids(decade_key)
        print(number_kids)

        for _ in range(number_kids):
            self.createChildren(Molly_Jones.year_born,Molly_Jones)

        Desmond_Jones.children =  Molly_Jones.children



        #Tree Building
        # Looked up built in python queue found at https://www.geeksforgeeks.org/python/queue-in-python/
        queue = deque()
        
        for child in Molly_Jones.children:
            queue.append(child)

        while queue:

            curr_person = queue.popleft()
            _, is_married = self.chance_kids(self.get_decade(curr_person.year_born))

            if is_married == "marry":
                curr_person.partner = self.createChildren(curr_person.year_born + random.randint(-10,10), None)
                if curr_person.partner == None:
                    break
                curr_person.partner.partner = curr_person


                if curr_person.age > curr_person.partner.age:
                    number_kids,_ = self.chance_kids(self.get_decade(curr_person.year_born))
                    for _ in range(number_kids):
                        new_child = self.createChildren(curr_person.year_born,curr_person)

                        if new_child == None:
                            continue
                        
                        print("Married:", new_child.year_born, new_child.firstN)
                        #for child in curr_person.children:
                        queue.append(new_child)
                    curr_person.partner.children = curr_person.children

                elif curr_person.age <= curr_person.partner.age:
                    number_kids,_ = self.chance_kids(self.get_decade(curr_person.partner.year_born))
                    for _ in range(number_kids):
                        new_child = self.createChildren(curr_person.partner.year_born,curr_person.partner)

                        if new_child == None:
                            break
                       
                        print("Married:", new_child.year_born, new_child.firstN)
                        #for child in curr_person.partner.children:
                        queue.append(new_child)
                    curr_person.children = curr_person.partner.children

            else:
                number_kids, _ = self.chance_kids(self.get_decade(curr_person.year_born))
                for _ in range(number_kids):
                    new_child = self.createChildren(curr_person.year_born,curr_person)

                    if new_child == None:
                        continue
                    print("UnMarried:", new_child.year_born, new_child.firstN)
                    
                    queue.append(new_child)

          
    def createChildren(self,Elder_Age,Parent):
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
        
        death = year_born + float(self.lifeProb[str(year_born)])+ random.randint(-10,10) 
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
        gender_vals = self.genderProb[decade]
        
        
        genders = [item[0] for item in gender_vals]
        freq = [item[1] for item in gender_vals]
        
        gender = random.choices(genders, weights=freq, k=1)[0]
        return gender
        
    def get_decade(self,year):
        decade_int = (year // 10) * 10
        decade_key = str(decade_int) + "s"
        
        return decade_key
    
    def first_gen(self, decade,gender):
             
        gendered_options = [val for val in self.firstNames[decade] if val[0] == gender]
   
        first_names = [val[1] for val in gendered_options]
        freq = [val[2] for val in gendered_options]


        name = random.choices(first_names, weights=freq, k=1)[0]
        return name
        
    def get_random_last_name(self,decade):
        lastNames = self.lastNames[decade]
        
        
        list_last_names = [item[1] for item in lastNames]

        random.shuffle(list_last_names)
        name = list_last_names.pop()
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
            self.firstNames[rows[0]].append((rows[1],rows[2],float(rows[3])))
        
        for rows in self.load_csv('gender_name_probability.csv'):
            self.genderProb[rows[0]].append((rows[1],float(rows[2])))
                                             
        for rows in self.load_csv('last_names.csv'):
            self.lastNames[rows[0]].append((rows[1],rows[2]))
                                        
        for rows in self.load_csv('life_expectancy.csv'):
            self.lifeProb[rows[0]] = (rows[1]) 
            
        
            
  
