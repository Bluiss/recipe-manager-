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
            findRecipe()
            break
        elif startAnswer.lower() == "3":
            print("Meal Plan")
            break
        else:
            print("Opps, try again either 1,2 or 3")

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
    
    columnList = ["(1) Name","(2) Total Time","(3) Cuisine","(4) Dietary Restrictions", "(3)Rating"]
    print("How would you like to search for a new recipe?")
    print(*columnList, sep="\n")

    
    values_list = worksheet.col_values(5)
    print(values_list)


def main():
    print_pause("Weclome to the Recipe Manager! ")
    print_pause("We have hundreds of recipes you can look into ")
    startManager()

main()