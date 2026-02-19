from collections import defaultdict, deque
import random
from Person_Factory_class import PersonFactory


class FamilyTree():
    
    def __init__(self):
        self.person1 = None
        self.person2 = None
        self.list_people = []

        self.Person_Factory = PersonFactory()
        self.Person_Factory.get_files()

    def create_initial_people(self):
        # Create the initial people
        Desmond_Jones = self.Person_Factory.create_person(None,None)
        Desmond_Jones.firstN, Desmond_Jones.lastN  = "Desmond", "Jones"
        
        Molly_Jones = self.Person_Factory.create_person(None,None)
        Molly_Jones.firstN, Molly_Jones.lastN  = "Molly", "Jones"
       
        #initial Partner assignment
        Desmond_Jones.partner, Molly_Jones.partner = Molly_Jones, Desmond_Jones

        self.person1, self.person2 = Desmond_Jones,  Molly_Jones
        #initial Children 
        year = Molly_Jones.year_born
        decade_key = self.Person_Factory.get_decade(year)
    
        number_kids,_ = self.Person_Factory.chance_kids(decade_key)
      
        # Create the children for the initial people
        for _ in range(number_kids):
            self.Person_Factory.create_person(Molly_Jones.year_born,Molly_Jones)

        # Add the children to the list of people
        Desmond_Jones.children =  Molly_Jones.children
        # Add the initial people to the list of people
        self.list_people.append(Desmond_Jones)
        self.list_people.append(Molly_Jones)


    def create_family_tree(self, Parent):
        #Tree Building
        # Looked up built in python queue found at https://www.geeksforgeeks.org/python/queue-in-python/
        queue = deque()
        

        for child in Parent.children:
            queue.append(child)

        # Build the tree with Queue implementation
        # queue loops until it is empty, removing the first person and adding their children to the queue
        while queue:
            
            curr_person = queue.popleft()
            # Add the current person to the list of people
            self.list_people.append(curr_person)

         
            _, is_married = self.Person_Factory.chance_kids(self.Person_Factory.get_decade(curr_person.year_born))


            elder_parent = None
            if is_married == "marry":

                curr_person.partner = self.Person_Factory.create_person(curr_person.year_born + random.randint(-10,10), None)
                if curr_person.partner == None:
                    continue
                self.list_people.append(curr_person.partner)
                curr_person.partner.partner = curr_person
                # Determine the elder parent
                if curr_person.age >= curr_person.partner.age:
                    elder_parent = curr_person
                else:
                    elder_parent = curr_person.partner
            else:
                elder_parent = curr_person
            
            # Chance the kids for the elder parent
            number_kids,_ = self.Person_Factory.chance_kids(self.Person_Factory.get_decade(elder_parent.year_born))
            for _ in range(number_kids):
                new_child = self.Person_Factory.create_person(elder_parent.year_born,elder_parent)

                if new_child == None:
                    continue
                
              
                queue.append(new_child)
            if is_married == "marry":
                elder_parent.partner.children = elder_parent.children 

        # Print the tree
    def print_tree(self, person = None, space=0):
        
        if person == None:
            person = self.person1
        if person.partner:
            print("    " * space, "-Parents:", person.firstN, person.lastN,  "Life: (", person.year_born, "-", person.death, ") |Partner:",person.partner.firstN, person.partner.lastN )
        else:
            print("     " * space, "-Parents:", person.firstN, person.lastN, "Life: (", person.year_born, "-", person.death, ")"  )
    
        for child in person.children:
            self.print_tree(child, space + 1)
    # Print the number of people in the tree
    def number_of_people_in_tree(self):
        return len(self.list_people)
    
    # Print the number of people in the tree per decade
    def number_people_in_year(self):
        by_year = defaultdict(int)

        for person in self.list_people:
            by_year[self.Person_Factory.get_decade(person.year_born)] += 1 
        
        for key in by_year:
            print("For year:",key,"is",by_year[key])
            
    # Print the number of duplicates in the tree
    def duplicates_names(self):
        by_year = defaultdict(int)

        for person in self.list_people:
            full_name = person.firstN + " " + person.lastN 
            by_year[full_name] += 1 
        total_duplicates = 0
        
        for key in by_year:
            if by_year[key] > 1:
                print("The name",key , "is Duplicated", by_year[key], "times")
                total_duplicates += 1
        print("Total duplicates:", total_duplicates)
        
        
        
        