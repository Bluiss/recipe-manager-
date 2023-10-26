import gspread


sa = gspread.service_account(filename='creds.json')
sh = sa.open("recipe_manager")
worksheet = sh.worksheet('Sheet1')
data = worksheet.get_all_records(default_blank=True)



def recipeSearch():
    """
    Search for a recipe based on the cuisine
    """
    while True:
        print("What Cuisine would you like to eat?\n")

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


recipeSearch()