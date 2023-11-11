import gspread
import time
import random
from google.oauth2 import service_account
from googleapiclient.discovery import build
from rich.console import Console
from rich.table import Table

console = Console()


sa = gspread.service_account(filename='creds.json')
sh = sa.open("recipe_manager")
worksheet = sh.worksheet('Sheet1')
data = worksheet.get_all_records(default_blank=True)

def displayTable(header, rows, title="Recipes"):
    table = Table(title=title)

    for column in header:
        table.add_column(column)
    
    for row in rows:
        row_values = [str(row.get(column, "")) for column in header]
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
        startAnswer = input("what would you like to do?\n (1)Add or Remove a recipe?\n (2)Search for a Recipe?\n (3)Meal plan a week?\n")
        if startAnswer.lower() == "1":
            addRemoveRecipe()
            break
        elif startAnswer.lower() == "2":
            findRecipe()
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



def addRecipe():
        """
        Allows the user to add a new recipe based on the pre existing columns
        """
        name = input("Please Enter the Recipes name: ").strip()
        ingredients = input("Please Enter the Ingredients: ").strip()
        instructions = input("Enter in the recipes instructions : ").strip()
        time = input("Total time it takes to cook : ").strip()
        servings = input("Total Servings : ").strip()
        cuisine = input("What cuisine is it? : ").strip()
        dietaryRestrictions = input("Any Dietary restrictions? : ").strip()
        rating =  input("Finally, how good is it. Give it a rating out of 5!: ").strip()

        if not name:
            raise ValueError("Recipe name cannot be empty")
        
        next_row = len(data) + 2

        values = [[name, ingredients, instructions, time, servings, cuisine, dietaryRestrictions, rating]]
        worksheet.insert_rows(values, row=next_row)
        print("Recipe added successfully!")
    
        startManager()


def findRecipe():
    """
    searches through all the columns for a specifc recipe 
    """
    column_search_name = input("How would you like to search through the recipes? \n Name \n Cook Time \n Cuisine \n Dietary Restrictions \n ")
    search_value = input("What are you searching for?: ").lower().replace(" ", "")

    found_rows = []
    column_index = None

    for col, header in enumerate(worksheet.get_all_values()[0]):
        if header.lower() == column_search_name.lower(): 
            column_index = col
            break

    if column_index is not None:
        for row in worksheet.get_all_values():
            if row[column_index].lower() == search_value:
                found_rows.append(row)
    
        if found_rows:
            header = worksheet.get_all_values()[0]
            displayTable(header, found_rows)

        
        else:
            print(f"Sorry, theres no rows in '{column_search_name}' column that contain '{search_value}'.")

    
    else:
        print(f"{column_search_name}' not found in the database.")

    startManager()


def deleteRecipe():
    """
    Deletes a recipe from the databse, by searching for its name
    """
    deleteSearch = input("What recipe would you like to delete?: ").lower().replace(" ", "")

    deleteFound = []
    for index, row in enumerate(worksheet.get_all_values(), start=1):
        row_lower = [cell.lower() for cell in row]
        if deleteSearch in row_lower:
            deleteFound.append(index)


    for found_row_index in deleteFound:
        print(worksheet.row_values(found_row_index))
        delete_answer = input("Would you like to delete this recipe? Y/N")

        if delete_answer.upper() == "Y":
            worksheet.delete_rows(found_row_index)
            print("Recipe deleted.")
            startManager()
        else:
            deleteReset()
    
def deleteReset():
    delete_answer_input = input("Did you still want to delete a recipe? Y/N")
    if delete_answer_input.upper() == "Y":
        deleteRecipe()
    else:
        startManager()


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
                displayTable(["Name", "Ingredients", "Instructions", "Cook Time", "Servings", "Cuisine", "Dietary Restrictions", "Rating"], random_rows, f"Day {day}")
            break 
        else:
            print("Please select a plan between 1 & 7 days")

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