
# Testing

Once the portal was operational I set about testing it for errors and to ensure any possible errors that can be made were caught.

| Feature              | Action                                        | Expected Result                                                                                                          | Works |
|----------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|-------|
| Add recipe           | Add a recipe to database                      | Adds a recipe to the database with specifc columns and a randomly generated id                                           | Y     |
| Remove recipe        | removes recipe from the databse               | Searches for a recipes by name, gives the user all associated recipes and asks for an id to be removed from the databse  | y     |
| Meal planner         | Plans meals for X days                        | Creates a meal plan, with 3 meals per day based on a set amount of days input by the user                                | y     |
| Search for recipes   | Search for reciepes based on search criteria  | Allows the user to search for recipes based on a set amount of criteria eg name                                          | Y     |
| Favourite a recipe   | Favourite a recipe                            | Favourites a recipe and adds it to a seperate worksheet                                                                  | y     |
| View all favourites  | Shows all recipes on the favourites tab       | Shows all recipes on the favourites tab                                                                                  | y     |

## Testing Browsers
The portal was tested in the following browsers (based on my own testing and those of people who tested the portal):

- Chrome
- Safari

It worked without issues in the above browsers.

## Testing Google Sheets

Once the Google sheets was attached and working I tested the system several times by including test recipes and removing them 


