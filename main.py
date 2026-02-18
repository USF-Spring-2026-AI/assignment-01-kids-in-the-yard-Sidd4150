from FamilyTree_class import FamilyTree

familyCreation = FamilyTree()

familyCreation.create_initial_people()
familyCreation.create_family_tree(familyCreation.person1)
# familyCreation.print_tree()
# print(familyCreation.number_of_people_in_tree())
# familyCreation.number_people_in_year()
# familyCreation.duplicates_names()

print("\nTree built")
while True:
    print("Welcome to family tree")
    print("(N) for number of people in the tree")
    print("(Y) for number of people in the tree per year")
    print("(D) for number of people duplicate people")
    print("(P) to print tree\n")
    choice = input("Selection: ").strip().upper()

    if choice == 'N':
        # Calling your method to get the total count
        count = familyCreation.number_of_people_in_tree()
        print(f"\nTotal people in the tree: {count}")

    elif choice == 'Y':
        # This calls your method that prints people per year
        print("\nPeople born per year:")
        familyCreation.number_people_in_year()

    elif choice == 'D':
        # Shows duplicate name statistics
        print("\nChecking for duplicate names...")
        familyCreation.duplicates_names()

    elif choice == 'P':
        # Visualizes the tree
        print("\nVisual Family Tree:")
        familyCreation.print_tree()

    elif choice == 'Q':
        print("Exiting... Goodbye!")
        break # Breaks the while loop to end the program

    else:
        print("Invalid selection. Please try again.")

    print()