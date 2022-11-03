import psycopg
from psycopg import OperationalError
import os
import sys

def create_connection(db_name, db_user, db_password, db_host = "localhost", db_port = "5432"):
    connection = None
    try:
        connection = psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        #print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(query, params=None):
    connection = create_connection("postgres", "postgres", "postgres")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        #print("Query executed successfully")
        connection.close()
        return cursor
    except OSError as e:
        print(f"The error '{e}' occurred or the hero name is already taken")
    except NameError as e:
        print(f"This was a name error.")

# ------------------------------------------------- DON'T CHANGE ANYTHING ABOVE THIS LINE --------------------------------------------

# first_query = "SELECT * FROM heroes"
# returned_vals = execute_query(first_query)
# for x in returned_vals:
#     print(x)

def select_all_heroes():
    query = """
        SELECT * from heroes
    """

    returned_items = execute_query(query).fetchall()
    for item in returned_items:
        print(item[1])

def select_all_abilities():
    query = """
        SELECT * from ability_types
    """

    returned_items = execute_query(query).fetchall()
    for item in returned_items:
        print(item[1])

def search_by_name(name_in):
    query = """
        SELECT %s FROM heroes
    """
    returned_items = execute_query(query, (name_in,)).fetchall()
    for item in returned_items:
        print(item[0])
    input()
    os.system('clear')
    title_screen()
    menu_list()

def create_new_superhero(name_in, about_in, bio_in):
    query = """
        INSERT INTO heroes (name, about_me, biography)
        VALUES (%s, %s, %s)
        """
    execute_query(query, (name_in, about_in, bio_in))
    print("")
    print(name_in + " has been added to the database! Choose option 2 from the main menu to verify.")
    input()
    os.system('clear')
    title_screen()
    menu_list()

def lookup_name_by_id(id_in):
    query = """
        SELECT name FROM heroes WHERE id=%s
        """
    returned_items = execute_query(query, (id_in,)).fetchall()

    return(returned_items[0][0])

def lookup_id_by_name(name_in):
    query = """
        SELECT id FROM heroes WHERE name=%s
        """
    returned_items = execute_query(query, (name_in,)).fetchall()

    return(returned_items[0][0])

def add_a_relationship(hero1, hero2, rel_type):
    query = """
        INSERT INTO relationships (hero1_id, hero2_id, relationship_type_id)
        VALUES (%s, %s, %s)
        """
    execute_query(query, (hero1, hero2, rel_type))

def add_an_ability(hero_id, ability_id):
    query = """
        INSERT INTO abilities (hero_id, ability_type_id)
        VALUES (%s, %s)
        """
    execute_query(query, (hero_id, ability_id))
    hero_name = lookup_name_by_id(hero_id)
    ability_name = lookup_ability_by_id(ability_id)
    print("")
    print(hero_name, " has been given the power of ", ability_name, "!")
    print("View the profile again to verify (Main Menu option 1).")
    input()

def remove_an_ability(hero_id, ability_id):
    query = """
        DELETE FROM abilities WHERE hero_id = %s AND ability_type_id = %s
        """
    execute_query(query, (hero_id, ability_id))
    hero_name = lookup_name_by_id(hero_id)
    ability_name = lookup_ability_by_id(ability_id)
    print("")
    print(hero_name, " no longer has the power of ", ability_name, "!")
    print("View the profile again to verify (Main Menu option 1).")
    input()


def lookup_ability_by_id(id_in):
    query = """
        SELECT name FROM ability_types WHERE id=%s
        """
    returned_items = execute_query(query, (id_in,)).fetchall()

    return(returned_items[0][0])

def lookup_id_by_ability(ability_name_in):
    query = """
        SELECT id FROM ability_types WHERE name=%s
        """
    try:
        returned_items = execute_query(query, (ability_name_in,)).fetchall()
    except NameError as e:
        print(f"This was a name error: {e}")

    return(returned_items[0][0])

def show_profile(name_in):
    # This function takes in the name of the superhero
    # and returns their about me and biography, a list of their superpowers,
    # and a list of their alliances
    os.system('clear')
    title_screen()
    print("")
    query = """
        SELECT name, about_me, biography FROM heroes WHERE name = %s
        """
    returned_items = execute_query(query, (name_in,)).fetchall()
    print("")
    print("Name:\t", returned_items[0][0])
    print("")
    print("About:\t", returned_items[0][1])
    print("")
    print("Biography:\n", returned_items[0][2])

    query = """
        SELECT heroes.name, ability_types.name FROM heroes 
            JOIN abilities ON hero_id = heroes.id
            JOIN ability_types on ability_types.id = abilities.ability_type_id
            WHERE heroes.name = %s
        """
    returned_items = execute_query(query, (name_in,)).fetchall()
    print("")
    print("Superpowers:")
    for item in returned_items:
        print("\t", item[1])

    query = """
        SELECT heroes.name, relationship_types.name, relationships.hero2_id FROM heroes
            JOIN relationships ON relationships.hero1_id = heroes.id
            JOIN relationship_types on relationship_types.id = relationships.relationship_type_id
        WHERE heroes.name = %s
        """
    returned_items = execute_query(query, (name_in,)).fetchall()
    print("")
    print("Friends:")
    for item in returned_items:
        if item[1]=="Friend":
            friend_name = lookup_name_by_id(item[2])
            print("\t", friend_name)
    print("")
    print("Enemies:")
    for item in returned_items:
        if item[1]=="Enemy":
            enemy_name = lookup_name_by_id(item[2])
            print("\t", enemy_name)

    print("")
    choice = input("""
1.) Modify Relationships
2.) Modify Superpowers
3.) Return to the Main Menu

""")
    match choice:
        case "1":
            print("")
            hero_2_name = input("Enter the other hero's name (Or enter <L> to see a list): ")
            if hero_2_name.upper() == "L":
                print("")
                print("SUPERHEROES:")
                select_all_heroes()
                print("")
                hero_2_name = input("Enter the other hero's name: ")
            relationship_choice = input("Is this a <F>riendship or are they <E>nemies? ").upper()
            if relationship_choice == "F":
                relationship_type = 1
            elif relationship_choice == "E":
                relationship_type = 2
            else:
                print("Sorry, invalid selection.")
                input()
                os.system('clear')
                title_screen()
                menu_list()
            hero_1_id = lookup_id_by_name(name_in)
            hero_2_id = lookup_id_by_name(hero_2_name)
            add_a_relationship(hero_1_id, hero_2_id, relationship_type)
            print("")
            print("New relationship added! View the profile again to verify (Main Menu option 1).")
            input()
            os.system('clear')
            title_screen()
            menu_list()

        case "2":
            print("")
            choice = input("<A>dd a new ability or <R>emove an existing ability? ")
            if choice.upper() == "A":
                hero_id = lookup_id_by_name(name_in)
                ability_name = input("Enter the new ability (or enter <L> to see a list): ")
                if ability_name.upper() == "L":
                    print("")
                    print("ABILITIES:")
                    select_all_abilities()
                    print("")
                    ability_name = input("Enter the new ability: ")
                ability_id = lookup_id_by_ability(ability_name)
                add_an_ability(hero_id, ability_id)
                input()
                os.system('clear')
                title_screen()
                menu_list() 
            elif choice.upper() == "R":
                hero_id = lookup_id_by_name(name_in)
                ability_name = input("Enter the ability to be removed: ")
                ability_id = lookup_id_by_ability(ability_name)
                remove_an_ability(hero_id, ability_id)
                input()
                os.system('clear')
                title_screen()
                menu_list() 
            else:
                print("")
                print("Sorry, that was an invalid entry.")
                input()
                os.system('clear')
                title_screen()
                menu_list() 

        case "3":
            os.system('clear')
            title_screen()
            menu_list()
        
    print("")
    print("Sorry, that was an invalid entry.")
    input()
    os.system('clear')
    title_screen()
    menu_list()    

def all_superheroes_with_abilities():
    title_screen()
    print("")
    query = """
        SELECT heroes.name, ability_types.name FROM heroes
        JOIN abilities ON abilities.hero_id = heroes.id
        JOIN ability_types ON ability_types.id = abilities.ability_type_id;
        """
    print("")
    returned_items = execute_query(query).fetchall()
    #print(returned_items)
    for item in returned_items:
        print(item[0] + "\t \t" + item[1])
        #print(item[0][0], item[1][1])
        #print(item[2])
    input()
    os.system('clear')
    title_screen()
    menu_list()

def delete_superhero(name_in):
    query = """
        DELETE FROM heroes WHERE name = %s
        """
    execute_query(query, (name_in,))
    print("")
    print(name_in, " has been eradicated. Use Main Menu option 2 to verify.")
    input() 
    os.system('clear')
    title_screen()
    menu_list()

def title_screen():
    os.system("clear")
    # print("")
    # print(" ")
    # print(" ◈ ◈ ◈ ◈ ◈ ╔══════════════╗ ◈ ◈ ◈ ◈ ◈")
    # print("╒══════════╝  SUPERHEROES ╚══════════╕")
    # print("│                 NET                │")
    # print("╞════════════════════════════════════╡")
    print("  ______                                      __    __            __")
    print(" /      \\                                    |  \\  |  \\          |  \\")
    print("|  ▓▓▓▓▓▓\\__    __  ______   ______   ______ | ▓▓\\ | ▓▓ ______  _| ▓▓_")   
    print("| ▓▓___\\▓▓  \\  |  \\/      \\ /      \\ /      \\| ▓▓▓\\| ▓▓/      \\|   ▓▓ \\")  
    print(" \\▓▓    \\| ▓▓  | ▓▓  ▓▓▓▓▓▓\\  ▓▓▓▓▓▓\\  ▓▓▓▓▓▓\\ ▓▓▓▓\\ ▓▓  ▓▓▓▓▓▓\\\\▓▓▓▓▓▓") 
    print("  \\▓▓▓▓▓▓\\ ▓▓  | ▓▓ ▓▓  | ▓▓ ▓▓    ▓▓ ▓▓   \\▓▓ ▓▓\\▓▓ ▓▓ ▓▓    ▓▓ | ▓▓ __") 
    print("|  \\__| ▓▓ ▓▓__/ ▓▓ ▓▓__/ ▓▓ ▓▓▓▓▓▓▓▓ ▓▓     | ▓▓ \\▓▓▓▓ ▓▓▓▓▓▓▓▓ | ▓▓|  \\")
    print(" \\▓▓    ▓▓\\▓▓    ▓▓ ▓▓    ▓▓\\▓▓     \\ ▓▓     | ▓▓  \\▓▓▓\\▓▓     \\  \\▓▓  ▓▓")
    print("  \\▓▓▓▓▓▓  \\▓▓▓▓▓▓| ▓▓▓▓▓▓▓  \\▓▓▓▓▓▓▓\\▓▓      \\▓▓   \\▓▓ \\▓▓▓▓▓▓▓   \\▓▓▓▓") 
    print("                  | ▓▓")                                                   
    print("                  | ▓▓")                                                   
    print("                   \\▓▓")                                                   
    print("╒═════════════════════════════════════════════════════════════════════════╕")
    print("│                SUPER SOCIAL NETWORKING FOR SUPERHEROES                  │")
    print("╘═════════════════════════════════════════════════════════════════════════╛")
    print("")

def menu_list():
    choice = input("""
1.) Display/Modify a Superhero Profile
2.) List all Superheroes
3.) List all Abilities
4.) Create a New Superhero Profile
5.) List Superheroes With Abilities
6.) Remove a Superhero

0 (zero) to Exit.

Enter your selection: """)

    match choice:
        case "1":
            print("")
            name_in = input("Superhero's User Name (or enter <L> for a list): ")
            if name_in.upper() == "L":
                print("")
                print("SUPERHEROES:")
                select_all_heroes()
                print("")
                name_in = input("Superhero's User Name: ")
            show_profile(name_in)

        case "2":
            title_screen()
            print("")
            print("SUPERHEROES:")
            select_all_heroes()
            input()
            os.system('clear')
            title_screen()
            menu_list()

        case "3":
            title_screen()
            print("")
            print("ABILITIES:")
            select_all_abilities()
            input()
            os.system('clear')
            title_screen()
            menu_list()

        case "4":
            title_screen()
            print("")
            name_in = input("Enter the superhero's name: ")
            about_in = input("Enter a brief 'about me' section: ")
            bio_in = input("Enter a more detailed biography: ")
            create_new_superhero(name_in, about_in, bio_in)

        case "5":
            title_screen()
            print("")
            all_superheroes_with_abilities()

        case "6":
            title_screen()
            print("")
            print("THANOS MODE ACTIVATED.")
            name_in = input("Superhero to Eradicate? (Or enter <L> to see a list). ")
            if name_in.upper() == "L":
                print("")
                print("SUPERHEROES:")
                select_all_heroes()
                print("")
                name_in = input("Superhero's to Remove: ")
            delete_superhero(name_in)

        case "0":
            sys.exit()

    print("")
    input("Sorry, that was an invalid entry.")
    os.system('clear')
    title_screen()
    menu_list()    

# ------------------------------------ ACTUAL MAIN PROGRAM -----------------------------------------------

title_screen()
menu_list()

input()
os.system('clear')
