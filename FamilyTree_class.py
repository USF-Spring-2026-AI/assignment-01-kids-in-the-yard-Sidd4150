

from collections import deque
import random
from Person_Factory_class import PersonFactory


class FamilyTree():
    
    def __init__(self):
        self.person1 = None
        self.person2 = None
       
        self.Person_Factory = PersonFactory()
        self.Person_Factory.get_files()
    def create_initial_people(self):
       
        Desmond_Jones = self.Person_Factory.createChildren(None,None)
        Desmond_Jones.firstN, Desmond_Jones.lastN  = "Desmond", "Jones"
        
        Molly_Jones = self.Person_Factory.createChildren(None,None)
        Molly_Jones.firstN, Molly_Jones.lastN  = "Molly", "Jones"
       
        #initial Partner assignment
        Desmond_Jones.partner = Molly_Jones
        Molly_Jones.partner = Desmond_Jones
        self.person1 = Desmond_Jones
        self.person2 = Molly_Jones
        
        #initial Children 
        year = Molly_Jones.year_born
        decade_key = self.Person_Factory.get_decade(year)
        print(decade_key)
        
        number_kids,_ = self.Person_Factory.chance_kids(decade_key)
        print(number_kids)

        for _ in range(number_kids):
            self.Person_Factory.createChildren(Molly_Jones.year_born,Molly_Jones)

        Desmond_Jones.children =  Molly_Jones.children


    def create_family_tree(self, Parent):
        #Tree Building
        # Looked up built in python queue found at https://www.geeksforgeeks.org/python/queue-in-python/
        queue = deque()
        
        for child in Parent.children:
            queue.append(child)

        while queue:

            curr_person = queue.popleft()
            _, is_married = self.Person_Factory.chance_kids(self.Person_Factory.get_decade(curr_person.year_born))

            if is_married == "marry":
                curr_person.partner = self.Person_Factory.createChildren(curr_person.year_born + random.randint(-10,10), None)
                if curr_person.partner == None:
                    break
                curr_person.partner.partner = curr_person
 
                elder_parent = None
            
                if curr_person.age >= curr_person.partner.age:
                    elder_parent = curr_person
                else:
                    elder_parent = curr_person.partner
 
                number_kids,_ = self.Person_Factory.chance_kids(self.Person_Factory.get_decade(elder_parent.year_born))
                for _ in range(number_kids):
                    new_child = self.Person_Factory.createChildren(elder_parent.year_born,elder_parent)

                    if new_child == None:
                        continue
                    
                    print("Married:", new_child.year_born, new_child.firstN)
                    #for child in curr_person.children:
                    queue.append(new_child)
                elder_parent.partner.children = elder_parent.children


            else:
                number_kids, _ = self.Person_Factory.chance_kids(self.Person_Factory.get_decade(curr_person.year_born))
                for _ in range(number_kids):
                    new_child = self.Person_Factory.createChildren(curr_person.year_born,curr_person)

                    if new_child == None:
                        continue
                    print("UnMarried:", new_child.year_born, new_child.firstN)
                    
                    queue.append(new_child)
    def print_tree(self, person = None, space=0):
        
        if person == None:
            person = self.person1
        if person.partner:
            print("    " * space, "|___Parents:", person.firstN, person.lastN,  "Life: (", person.year_born, "-", person.death, ") |Partner:",person.partner.firstN, person.partner.lastN )
        else:
            print("     " * space, "|___Parents:", person.firstN, person.lastN, "Life: (", person.year_born, "-", person.death, ")"  )
    
        for child in person.children:
            self.print_tree(child, space + 1)

    def number_of_people_in_tree(self):
        pass
    def number_people_in_year(self):
        pass
        
        