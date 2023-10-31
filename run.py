import gspread


sa = gspread.service_account(filename='creds.json')
sh = sa.open("recipe_manager")
worksheet = sh.worksheet('Sheet1')
data = worksheet.get_all_records(default_blank=True)



def startManager():
    startAnswer = input("what would you like to do?\n (1)Create a recipe?\n (2)Search for a Recipe?\n (3)Meal plan a week?\n")
    if startAnswer.lower() == "1":
        print("create")
    elif startAnswer.lower() == "2":
        print("search")
    elif startAnswer.lower() == "3":
        print("Meal Plan")
    else:
        print("Please select an answer")



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
    print("Weclome to the Recepie Manager!")
    startManager()

main()