from FamilyTree_class import FamilyTree

familyCreation = FamilyTree()

familyCreation.create_initial_people()
familyCreation.create_family_tree(familyCreation.person1)
familyCreation.print_tree()