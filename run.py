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
    time.sleep(2)

def startManager():
    """
    Allows user to either search/create a recipe or creat a weekly meal plan 
    """
    while True:
        startAnswer = input("what would you like to do?\n (1)Create a recipe?\n (2)Search for a Recipe?\n (3)Meal plan a week?\n")
        if startAnswer.lower() == "1":
            print("create")
            break
        elif startAnswer.lower() == "2":
            selected_column = input("Enter your choice (or type 'exit' to quit): ")
            recipeSearch(data, selected_column)
            break
        elif startAnswer.lower() == "3":
            print("Meal Plan")
            break
        else:
            print("Opps, try again either 1,2 or 3")





def recipeSearch(data, column_name, search_value):
    matching_rows = [row for row in data if row.get(column_name) == search_value]

    if not matching_rows:
        print(f"Sorry, there's nothing in our database under {column_name} based on {search_value}")
    else:
        print(f"Please see all recipes associated with {search_value}")
        for row in matching_rows:
            print(row)

    while True:
        recipe_columns = ["Name", "Total Time", "Cuisine", "Dietary Restrictions"]
        for index, recipe_column in enumerate(recipe_columns, start=1):
            print(f"{index}. {recipe_column}")







def main():
    print_pause("Weclome to the Recpie Manager!")
    print_pause("we have thousands of recpies you can look into ")
    startManager()

main()