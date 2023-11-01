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
            cuisineRecipeSearch()
            break
        elif startAnswer.lower() == "3":
            print("Meal Plan")
            break
        else:
            print("Opps, try again either 1,2 or 3")




def cuisineRecipeSearch():
    """
    Search for a recipe based on the cuisine
    """
    while True:
        cuisines = ["American", "Asian", "Chinese", "Greek", "Hawaiian", "Indian", "Italian", "Mediterranean", "Mexican", "Russian", "Tex-mex", "Thai"]
        print("What Cuisine would you like to eat? \n")
        for index, cuisine in enumerate(cuisines, start=1):
            print(f"{index}. {cuisine}")

        search_value = input("Enter your Cuisine here:\n")

        if search_value.lower() == 'exit':
            break

        matching_rows = [row for row in data if row["Cuisine"] == search_value]
        
        if not matching_rows:
            print("Try again, no cuisine matches that input")
        else:
            print("Here is all the", search_value, "food we have")
            for row in matching_rows:
                print(row)





def main():
    print_pause("Weclome to the Recepie Manager!")
    print_pause("we have thousands of recepies you can look into ")
    startManager()

main()