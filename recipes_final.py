import sqlite3

conn = sqlite3.connect("social_media.db")
cur = conn.cursor()

tables = ["recipes", "required", "ingredients"]
recipe_cols = ["r_id", "r_name", "description", "rating", "time", "servings"]
required_cols = ["r_id", "amount", "i_id"]
ingredient_cols = ["i_id", "i_name", "flavor", "type"]

def table_schema():
    exit = False
    while exit == False:
        print("The table schema will list the table name with all of its columns indented below.")
        print("Table Schema:")
        print("recipes-")
        print("    r_id")
        print("    r_name")
        print("    description")
        print("    rating")
        print("    time")
        print("    servings")
        print("required-")
        print("    r_id")
        print("    amount")
        print("    i_id")
        print("ingredients-")
        print("    i_id")
        print("    i_name")
        print("    flavor")
        print("    type")
        print("")
        print("a. Show Table Schema Again")
        print("b. Exit")
        good_input = False
        while good_input == False:
            user = input("=>")
            match user:
                case "a":
                    good_input = True
                case "b":
                    exit = True
                    good_input = True
                case _:
                    print("Please enter a or b")

def stats():
    options = ["mean", "min", "max", "median", "std"]

    valid = False
    while not valid:
        print("\nPlease choose a statistical query type:\n{options}")
        func = input("=> ")

        if func in options:
            valid = True
        else:
            print("Invalid choice")

    # Tweak to ensure column is numeric
    table, column = validate_table_col()

    # sql statement

    # print results

def where():
    table, column = validate_table_col()

    print("Please enter the condition for the WHERE statement")
    print("ex: 'time <= 60'")
    condition = input("=> ")

    # sql statement

    # print results

def validate_table_col():
    valid = False
    while not valid:
        print(f"\navailable tables:\n{tables}")
        table = input("Choose from the tables above ")

        if table in tables:
            valid = True
        else:
            print("Invalid choice")
    
    if table == tables[0]:
        cols = recipe_cols
    elif table == tables[1]:
        cols = required_cols
    else:
        cols = ingredient_cols

    valid = False
    while not valid:
        print(f"\navailable columns:\n{cols}")
        column = input("Choose from the columns above ")

        if column in cols:
            valid = True
        else:
            print("Invalid choice")
    
    return (table, column)

def main():
    print("Welcome to the Recipe Database!!")

    quit = False
    while quit == False:
        print("Please select one of the following options:")
        print("a. See Table Schema") #jes
        print("b. Add/Remove/Modify Tables") #jes
        print("c. See Basic Stats") #skye
        print("d. Make a Where Query") #skye
        print("e. See Ingredients of a Recipe") #jes
        print("f. See Recipes That Match Pantry") #skye
        print("g. See Data Visualizations") #jes
        print("h. Quit")

        user_input = input("=>")
        match user_input:
            case "a":
                table_schema()
            case "b":
                print("")
            case "c":
                print("")
            case "d":
                print("")
            case "e":
                print("")
            case "f":
                print("")
            case "g":
                print("")
            case "h":
                print("Logged Out Successfully!")
                quit = True
            case _:
                print("Please enter a, b, c, d, e, f, g or h")


if __name__ == '__main__':
    main()