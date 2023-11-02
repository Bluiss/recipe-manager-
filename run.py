import gspread
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build


sa = gspread.service_account(filename='creds.json')
sh = sa.open("recipe_manager")
worksheet = sh.worksheet('Sheet1')
data = worksheet.get_all_records(default_blank=True)



def print_pause(message):
    print(message)
    time.sleep(1)

def startManager():
    """
    Allows user to either search/create a recipe or creat a weekly meal plan 
    """
    while True:
        startAnswer = input("what would you like to do?\n (1)Create a recipe?\n (2)Search for a Recipe?\n (3)Meal plan a week?\n")
        if startAnswer.lower() == "1":
            addRecipe()
            break
        elif startAnswer.lower() == "2":
            selected_column = input("")
            recipeSearch(data, selected_column)
            break
        elif startAnswer.lower() == "3":
            print("Meal Plan")
            break
        else:
            print("Opps, try again either 1,2 or 3")

def addRecipe():
    name = input("Please Enter the recipes name: ").strip()
    ingredients = input("Please Enter the ringredients: ").strip()
    instructions = input("Enter in the recipes instructions : ").strip()
    time = input("Total time it takes to cook : ").strip()
    servings = input("Total Servings : ").strip()
    cuisine = input("What cuisine is it? : ").strip()
    dietaryRestrictions = input("Any Dietary restrictions? : ").strip()
    rating =  input("Finally, how good is it. Give it a rating out of 5!: ").strip()


    values = [[name, ingredients, instructions, time, servings, cuisine, dietaryRestrictions, rating]]
    worksheet.insert_rows(values, row=42)
    print("Recipe added successfully!")



def recipeSearch(data, column_name):
    matching_rows = [row for row in data if row.get(column_name) == {column_name}]

    if not matching_rows:
        print(f"Sorry, there's nothing in our database under {column_name} based on {column_name}")
    else:
        print(f"Please see all recipes associated with {column_name}")
        for row in matching_rows:
            print(row)

    while True:
        recipe_columns = ["Name", "Total Time", "Cuisine", "Dietary Restrictions"]
        for index, recipe_column in enumerate(recipe_columns, start=1):
            print(f"{index}. {recipe_column}")







def main():
    print_pause("Weclome to the Recipe Manager! ")
    print_pause("We have hundreds of recipes you can look into ")
    startManager()

main()