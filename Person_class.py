
class Person:
    def __init__(self, year_born, death, firstN, lastN, partner, children, age):
        self.year_born = year_born
        self.death = death
        self.firstN = firstN
        self.lastN = lastN
        self.partner = partner
        self.children = []
        self.age = age
        
    def print(self):
        print(self.partner)
    