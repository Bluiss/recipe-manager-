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
            for found_row in found_rows:
                print(found_row)
        
        else:
            print(f"Sorry, theres no rows in '{column_search_name}' column that contain '{search_value}'.")

    
    else:
        print(f"{column_search_name}' not found in the database.")

    startManager()


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