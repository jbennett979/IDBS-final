from math import sqrt
import sqlite3

conn = sqlite3.connect("recipes_final.db")
cur = conn.cursor()

db_schema = {
    "recipes" : {
        "r_id" : "numeric", 
        "r_name" : "text", 
        "description" : "text", 
        "rating" : "numeric", 
        "time" : "numeric", 
        "servings" : "numeric"
    },
    "required" : {
        "r_id" : "numeric",
        "amount" : "text",
        "i_id" : "numeric"
    },
    "ingredients" : {
        "i_id" : "numeric", 
        "i_name" : "text", 
        "flavor" : "text", 
        "type" : "text"
    }
}


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
            user = input("=> ")
            match user:
                case "a":
                    good_input = True
                case "b":
                    exit = True
                    good_input = True
                case _:
                    print("Please enter a or b")

def stats():
    options = ["mean", "min", "max", "median", "stdev"]

    table, column = validate_table_col(True)

    valid = False
    while not valid:
        print("\nPlease choose a statistical query type:")
        for f in options:
            print(f)
        func = input("=> ")

        if func in options:
            valid = True
        else:
            print("Invalid choice")

    if func == "mean":
        results = cur.execute(f"SELECT avg({column}) FROM {table}").fetchone()
    elif func == "median":
        results = cur.execute(f"SELECT {column} FROM {table} ORDER BY {column} LIMIT 1 OFFSET (SELECT count(*) FROM {table}) / 2").fetchone()
    elif func == "stdev":
        results = cur.execute(f"SELECT sum(({column} - mean.a) * ({column} - mean.a)), count(*)FROM {table}, (SELECT avg({column}) AS a FROM {table}) as mean").fetchone()

        results = (sqrt(results[0] / results[1]),)
    else:
        results = cur.execute(f"SELECT {func}({column}) FROM {table}").fetchone()

    # print results
    print(f"{func} of {table}.{column} = {results[0]}")
    input()

def where():
    table, column = validate_table_col()

    valid = False

    while not valid:
        print("\nPlease enter the condition for the WHERE statement")
        print("ex: 'time <= 60'")
        condition = input("=> ")

        # sql statement
        try:
            results = cur.execute(f"SELECT {column} FROM {table} WHERE {condition}").fetchall()
            valid = True
        except:
            print("Please enter a valid condition")

    # print results
    for item in results:
        print(item)

    input()

def validate_table_col(num_only = False):
    valid = False
    while not valid:
        print(f"\navailable tables:")
        for tab in db_schema:
            print(tab)
        table = input("Choose from the tables above: ")

        if table in db_schema:
            valid = True
        else:
            print("Invalid choice")

    cols = []
    
    valid = False
    while not valid:
        print(f"\navailable columns:")
        for col in db_schema[table]:
            if not num_only:
                cols.append(col)
                print(col)
            elif db_schema[table][col] == "numeric":
                cols.append(col)
                print(col)
                
        column = input("Choose from the columns above: ")

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

        user_input = input("=> ")
        match user_input:
            case "a":
                table_schema()
            case "b":
                print("")
            case "c":
                stats()
            case "d":
                where()
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

stats()

if __name__ == '__main__':
    main()