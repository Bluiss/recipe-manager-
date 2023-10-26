import gspread

sa = gspread.service_account(filename='creds.json')
sh = sa.open("recipe_manager")

wks = sh.worksheet('Sheet1')


print('Rows: ',wks.row_count)
print('Cols: ',wks.col_count)