import psycopg
from psycopg import OperationalError
import os

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
    input()
    os.system('clear')
    title_screen()
    menu_list()

def select_all_abilities():
    query = """
        SELECT * from ability_types
    """

    returned_items = execute_query(query).fetchall()
    for item in returned_items:
        print(item[1])
    input()
    os.system('clear')
    title_screen()
    menu_list()

def search_by_name(name_in):
    query = """
        SELECT %s FROM heroes
    """
    hero = execute_query(query, (name_in,)).fetchall()
    print(hero)
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

def all_superheroes_with_abilities():
    query = """
        SELECT name FROM heroes
        JOIN abilities ON id = hero_id
        """
    print("")
    returned_items = execute_query(query).fetchall()
    for item in returned_items:
        print(item[1])
        print(item[2])
    input()
    os.system('clear')
    title_screen()
    menu_list()

# select_all()

def title_screen():
    os.system("clear")
    print("")
    print("╒═══════════════╕")
    print("│SUPERHEROES NET│")
    print("╘═══════════════╛")
    print("")

def menu_list():
    choice = input("""1.) Search by Superhero Name
2.) List all Superheroes
3.) List all Abilities
4.) Enter a New Superhero
5.) List Superheroes With Abilities

Enter your selection: """)

    match choice:
        case "1":
            print("")
            search_name=input("Enter the superhero name: ")
            search_by_name(search_name)

        case "2":
            print("")
            print("SUPERHEROES:")
            select_all_heroes()

        case "3":
            print("")
            print("ABILITIES:")
            select_all_abilities()
        
        case "4":
            print("")
            name_in = input("Enter the superhero's name: ")
            about_in = input("Enter a brief 'about me' section: ")
            bio_in = input("Enter a more detailed biography: ")
            create_new_superhero(name_in, about_in, bio_in)
        
        case "5":
            print("")
            all_superheroes_with_abilities()


title_screen()
menu_list()


input()
os.system('clear')
