# SUPERNET: Super Social Networking for Superheroes
## Roger Mullins
## [Awesome Inc. Web Developer Bootcamp](https://www.awesomeinc.org/bootcamp) Fall '22 Cohort

*SUPERNET* is a command-line application that uses a SQL database backend to simulate a social network for superheroes. The interface gives the user the ability to manipulate and read from the database tables without the need to use complex SQL commands.

### Installation
*SUPERNET* requires the [Python3](https://www.python.org/downloads/) runtime environment, [postgreSQL](https://www.postgresql.org/), and the PIP package [psycopg](https://www.psycopg.org/) for communicating between the two. **The database must be created independently** once your environment is configured, using the SQL script [found here](https://drive.google.com/file/d/1ir7jg2KXJxtjTlP-ewY4blqXFC-Pok7d/view?usp=drive_web&authuser=0).

### Usage
The application launches into the Main Menu. From the Main Menu the following actions are possible:

- Main Menu
    1. [Display/Modify a Superhero Profile](#1-displaymodify-a-superhero-profile)
    1. [List all Superheroes](#2-list-all-superheroes)
    1. [List all Abilities](#3-list-all-abilities)
    1. [Create a New Superhero Profile](#4-create-a-new-superhero-profile)
    1. [List Superheroes With Abilities](#5-list-superheroes-with-abilities)
    1. [Remove a Superhero](#6-remove-a-superhero)

- **Entering 0 from the Main Menu will exit to your system prompt.**

#### 1. Display/Modify a Superhero Profile

- The heart of the program, this runs several queries on the database to display, on one screen, the Superhero's name, biographical information, superpowers and relationships. The superhero's exact name **must** be entered at the prompt; if you are unsure of how a superhero is listed, there is an option to display a list of all heros currently in the database.

- After the profile is displayed, there are three menu options:

1. Modify Relationships
    - This allows you to add a Friend or Enemy to the superhero's profile. 
    - Note that relationships in the **SUPERNET** world are somewhat one-sided; superhero A can add superhero B as a Friend or Enemy, but the relationsip will not appear on superhero B's profile unless it is explicitly added.
1. Modify Superpowers
    - This allows you to add or remove a superpower. Like searching for a profile, exact wording is important. If you are unsure how a particular ability is listed in the database, you have the option to display a list.
    - This routine only allows the selection of existing abilities. New global-level abilities cannot be defined here, nor can existing abilities be deleted. Those operations must be done from the Abilities menu option.
1. Return to the Main Menu

#### 2. List all Superheroes

#### 3. List all Abilities

- This menu option allows for the creation or deletion of superpowers.

1. Add a New Ability
1. Delete an Ability
    - Again, exact wording must be used. Refer to the list if you are unsure. 
    - Removing an ability will remove it from every superhero's profile.
1. Return to Main Menu

#### 4. Create a New Superhero Profile

- This menu option allows for the creation of a new superhero. You will be prompted to enter:

1. The superhero name
1. 'About Me'
    - Brief tagline
1. Biography
    - More in-depth information

- Note that relationships and abilities are **NOT** defined at this point; those must be added directly from the superhero's profile page (Main Menu option 1).

#### 5. List Superheroes With Abilities
- Use this to see a list of all superhero/ability pairings.

#### 6. Remove a Superhero
- This option allows you to completely remove a superhero from the database. The exact name must be entered; use the listing feature if you are unsure of how a superhero appears in the database.

### Contributions
Pull requests via the *SUPERNET* project's [public Github repository](https://github.com/rdmullins/sql-superheroes) are welcome!

### License
[MIT](https://choosealicense.com/licenses/mit/)
