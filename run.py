import gspread
import time
import random
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from rich.console import Console
from rich.table import Table



console = Console()


sa = gspread.service_account(filename='creds.json')
sh = sa.open("recipe_manager")
worksheet = sh.worksheet('Recipes')
worksheet_favourites = sh.worksheet('Favourites')
data = worksheet.get_all_records(default_blank=True)
df = pd.DataFrame(worksheet.get_all_records())

def displayTable(header, rows, title="Recipes"):
    table = Table(title=title)

    for column in header:
        table.add_column(column)

    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict):
                row_values = [str(row.get(column, "")) for column in header]
                table.add_row(*row_values)
            elif isinstance(row, list):
                table.add_row(*map(str, row))
    elif isinstance(rows, dict):
        row_values = [str(rows.get(column, "")) for column in header]
        table.add_row(*row_values)

    console.print(table)


def print_pause(message):
    console.print("[blue underline]" + message)
    time.sleep(1)

def startManager():
    """
    Allows user to either search/create a recipe or creat a weekly meal plan 
    """
    while True:
        startAnswer = input("What would you like to do?\n (1)Add or Remove a recipe?\n (2)Search for a Recipe?\n (3)Meal plan a week?\n")
        if startAnswer.lower() == "1":
            addRemoveRecipe()
            break
        elif startAnswer.lower() == "2":
            searchRecipe()
            break
        elif startAnswer.lower() == "3":
            mealPlanner(worksheet.get_all_records(default_blank=True))
            break
        else:
            print("Opps, try again either 1,2 or 3")

def addRemoveRecipe():
    """
    starts either ther add or remove recipe functions
    """
    ar = input("Would you like to add or remove a recipe? \n(1)Add \n(2)Remove\n")
    if ar == "1":
        addRecipe()
    elif ar == "2":
        deleteRecipe()

def idGenerate():
    """
    generates a random ID and checks against ID column in sheets, if false assigns value to new recipe
    """
    while True: 
        random_id = random.randint(1, 999)
        if(random_id in df['ID'].unique()) == False:
            return random_id


def addRecipe():
    """
    Allows the user to add a new recipe based on the pre-existing columns
    """
    while True:
        name = input("Please Enter the Recipes name: ").strip()
        ingredients = input("Please Enter the Ingredients: ").strip()
        instructions = input("Enter in the recipes instructions : ").strip()
        time = input("Total time it takes to cook : ").strip()
        servings = input("Total Servings : ").strip()
        cuisine = input("What cuisine is it? : ").strip()
        dietaryRestrictions = input("Any Dietary restrictions? : ").strip()
        rating = input("Finally, how good is it. Give it a rating out of 5!: ").strip()
        ID = idGenerate()

        next_row = len(data) + 2

        values = [name, ingredients, instructions, time, servings, cuisine, dietaryRestrictions, rating, ID]
        worksheet.insert_rows([values], row=next_row)

        message = f"Thanks for adding {name} to our database!"
        console.print("[blue underline]" + message)  

        displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating", "ID"], [values], "Added Recipe")

        print("Recipe added successfully!")

        another_recipe = input("Do you want to add another recipe? (yes/no): ").lower()
        if another_recipe != 'yes':
            startManager()
            break



def searchRecipe():
   """
   Starts either find new recipe or shows all favourited recipes 
   """
   while True:
        user_choice = input("Finding a favorite or looking for something new?\n(1) Find New Recipe\n(2) View all favorited recipes\n(3) Exit\n")
        if user_choice == "1":
            findRecipe()
        elif user_choice == "2":
            viewAllFavourites()
        elif user_choice == "3":
            print_pause("Goodbye!")
            startManager()
            break
        else:
            print("Oops, try again with 1, 2, or 3")


def findRecipe():
    """
    searches through all the columns for a specifc recipe 
    """
    while True:
        column_search_name = input("How would you like to search through the recipes? \n (1)Name \n (2)Cook Time \n (3)Cuisine \n (4)Dietary Restrictions \n ")
        if column_search_name.lower() == "1":
            nameSearch = input("Whats the recipes name?: ")
            searched_name = df[df['Name'].str.contains(nameSearch, case=False, na=False)].to_dict(orient='records')
            displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating", "ID"], searched_name, "Recipes")
            break
        elif column_search_name.lower() == "2":
            timeSearch = input("How long have you got to cook? Eg 10 mins: ")
            searched_time = df[df['Cook Time'].str.contains(timeSearch, case=False, na=False)].to_dict(orient='records')
            displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating","ID"], searched_time, "Recipes")
            break
        elif column_search_name.lower() == "3":
            cuisineSearch = input("Searching by cuisine? what are you after: ")
            searchedCuisine = df[df['Cuisine'].str.contains(cuisineSearch, case=False, na=False)].to_dict(orient='records')
            displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating", "ID"], searchedCuisine, "Recipes")
            break
        elif column_search_name.lower() == "4":
            drSearch = input("Have specific restrictions? Eg Vegetarian, Gluten Free..: ")
            searched_dr = df[df['Dietary Restrictions'].str.contains(drSearch, case=False, na=False)].to_dict(orient='records')
            displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating", "ID"], searched_dr, "Recipes")
            break
        else:
            print("Opps, try again either 1,2,3 or 4")

    recipeFound()


def recipeFound():
    while True:
        recipe_found_input= input("Found what you're after?\n(1)Yes let me favourite it\n(2)No I'll try again\n")
        if recipe_found_input.lower() == "1":
            favouriteRecipe()
            break
        elif recipe_found_input.lower() == "2":
            findRecipe()
            break
       
        else:
            print("Oops, try again with 1 or 2")

def favouriteRecipe():
    """
    Allows the user to select a favourite recipe and saves it to a list and sheet
    """
    id_search = input("Whats the ID of the recipe you want to save?: ")
    if int(id_search) in df.index:
        recipe_data = df.shift(periods=1).loc[[int(id_search)]]
        recipe_name = recipe_data['Name'].iloc[0]
        fav_message = f"You've added {recipe_name} to your favourites list, must be a tasty one!"
        displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating", "ID"], recipe_data, fav_message)
        worksheet_favourites.append_row(recipe_data.values.tolist()[0])
        print("Recipe added Sucessfully")

    else:
        print("Recipe not found with the provided ID.")

def viewAllFavourites():
    """
    Prints all rows from favourites worksheet
    """
    all_favourites = worksheet_favourites.get_all_records()
    displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating"], all_favourites, "Favourites")



def deleteRecipe():
    """
    Deletes a recipe from the databse, by searching for its name
    """
    deleteSearch = input("What recipe would you like to delete?: ")

    deleteFound = df[df['Name'].str.contains(deleteSearch, case=False, na=False)].to_dict(orient='records')

    if deleteFound:
        displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating", "ID"], deleteFound, "Recipes")
        deleteFoundRecipe()

    else:
        print("Sorry, theres no recipes matching that input.")

def deleteFoundRecipe():
    """
    Takes id from user input and deltes related recipe
    """
    delete_search = input("Whats the ID of the recipe you want to delete?: ")
    if int(delete_search) in df.index:
        delete_data = df.shift(periods=1).loc[[int(delete_search)]]
        recipe_name = delete_data['Name'].iloc[0]
        delete_message = f"{recipe_name} will be been removed from the database"
        displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating", "ID"], delete_data, delete_message)
        worksheet.delete_row(int(delete_data.index[0]))

        print("Recipe deleted Sucessfully")

    else:
        print("Recipe not found with the provided ID.")
   


def mealPlanner(data):
    """
    Meal plan for a specific amount of days input by the user (Source 1)
    """
    while True:
        days_input = int(input("How many days do you need meals for? "))
        if days_input in range(1, 8):
            days_list = generate_days_list(days_input)
            print("Meal plan for the following days:")
            for day in days_list:
                random.shuffle(data)
                random_rows = data[:3]
                displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating", "ID"], random_rows, f"Day {day}")
            break 
        else:
            print("Please select a plan between 1 & 7 days")

    while True:
        user_choice = input("Plenty of meals for {day} days, or did you need some more?\n(1)No all good, take me back to the main page\n(2)Need some more meals ")
        if user_choice == "1":
            startManager()
        elif user_choice == "2":
            mealPlanner(data)
        else:
            print("Oops, try again with 1 or 2")

def generate_days_list(days_input):
    i = 1
    dlist = []
    while i <= days_input:
        dlist.append(i)
        i += 1
    return dlist


    


def main():
    print_pause("Weclome to the Recipe Manager! ")
    print_pause("We have hundreds of recipes you can look into ")
    startManager()

main()