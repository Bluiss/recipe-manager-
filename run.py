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
            deleteRecipe()
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
    """
    It specifies the name of the column you want to search in (e.g., "Name") and the value you want to search for (e.g., "chicken").

    It finds the index of the specified column by iterating through the headers in the first row of the worksheet. The comparison is case-insensitive.

    If the specified column is found, it searches for the value in that column within each row and appends matching rows to the found_rows list. The comparison is case-insensitive.

    If any matching rows are found, it prints them. Otherwise, it prints a message indicating that no rows contain the specified value in the specified column.
    """
    
   


def deleteRecipe():
    """
    Deletes a recipe from the databse, by searching for its name
    """
    deleteSearch = input("What recipe would you like to delete?: ").lower()

    deleteFound = []
    for row in worksheet.get_all_values():
        row_lower = [cell.lower() for cell in row]
        if deleteSearch in row_lower:
            deleteFound.append(row)


    for found_row in deleteFound:
        print(found_row)


def main():
    print_pause("Weclome to the Recipe Manager! ")
    print_pause("We have hundreds of recipes you can look into ")
    startManager()

main()