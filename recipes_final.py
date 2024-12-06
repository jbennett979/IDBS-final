from math import sqrt
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect("recipes_final.db")
cur = conn.cursor()

tables = ["recipes", "required", "ingredients"]
recipe_cols = ["r_id", "r_name", "description", "rating", "time", "servings"]
required_cols = ["r_id", "amount", "i_id"]
ingredient_cols = ["i_id", "i_name", "flavor", "type"]

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

def change_tables():
    exit = False
    while exit == False:
        print("a. add")
        print("b. remove")
        print("c. modify")
        print("d. exit")
        choice = input("=> ")
        if choice == "a" or choice == "b" or choice == "c":
            valid = False
            while valid == False:
                print("Add/Remove/Modify from Tables:")
                print(f"\navailable tables:\n{tables}")
                table = input("Choose from the tables above ")
                if table in tables:
                    valid = True
                else:
                    print("Please enter a valid table")

            match choice:
                case "a":
                    add(table)
                case "b":
                    remove(table)
                case "_":
                    modify()
        elif choice == "d":
            exit = True
        else:
            print("Please enter a, b, c, or d")

def add(table):
    print(f"You chose to add an entry to the {table} table")
    if table == "recipes":
        while True:
            try:
                count = 0
                recipes_new_values = []
                for i in recipe_cols:
                    if recipe_cols[count] == "r_id" or recipe_cols[count] == "time" or recipe_cols[count] == "servings":
                        existing = True
                        while existing:
                            recipes_new_value = int(input(f"Entry for the {recipe_cols[count]} column: "))
                            if recipe_cols[count] == "r_id":
                                not_exists = f"SELECT count(r_id) FROM recipes WHERE r_id = {recipes_new_value}"
                                cur.execute(not_exists)
                                if cur.fetchone()[0] == 0:
                                    existing = False
                                else:
                                    print("Please enter an r_id not already in the table")
                            else:
                                existing = False
                    elif recipe_cols[count] == "rating":
                        recipes_new_value = float(input(f"Entry for the {recipe_cols[count]} column: "))
                    else:
                        recipes_new_value = input(f"Entry for the {recipe_cols[count]} column: ")
                    recipes_new_values.append(recipes_new_value)
                    count += 1
                break
            except ValueError:
                print("Please enter a number for the id, time, servings, and rating columns")
        recipes_query = f"INSERT INTO recipes VALUES ({recipes_new_values[0]},'{recipes_new_values[1]}','{recipes_new_values[2]}',{recipes_new_values[3]},{recipes_new_values[4]},{recipes_new_values[5]})"
        cur.execute(recipes_query)
        conn.commit()
    elif table == "required":
        while True:
            try:
                required_new_values = []
                count = 0
                for i in required_cols:
                    if required_cols[count] == "amount":
                        required_new_value = input(f"Entry for the {required_cols[count]} column: ")

                    else:
                        existing_entry = True
                        while existing_entry == True:
                            required_new_value = int(input(f"Entry for the {required_cols[count]} column: "))
                            if required_cols[count] == "i_id":
                                required_checker_query = f"SELECT count(i_id) FROM ingredients WHERE i_id = {required_new_value}"
                            elif required_cols[count] == "r_id":
                                required_checker_query = f"SELECT count(r_id) FROM recipes WHERE r_id = {required_new_value}"
                            cur.execute(required_checker_query)
                            required_checker = cur.fetchone()
                            r_check = required_checker[0]
                            if r_check == 0:
                                print("Please choose ingredients and recipes that already exist in the tables")
                            else:
                                existing_entry = False

                    required_new_values.append(required_new_value)
                    count += 1
                break
            except ValueError:
                print("Please enter a valid id")
        required_query = f"INSERT INTO required VALUES ({required_new_values[0]},'{required_new_values[1]}',{required_new_values[2]})"
        cur.execute(required_query)
        conn.commit()
    else:
        while True:
            try:
                ingredient_new_values = []
                counter = 0
                for i in ingredient_cols:
                    if ingredient_cols[counter] == "i_id":
                        existing_i = True
                        while existing_i:
                            ingredient_new_value = int(input(f"Entry for the {ingredient_cols[counter]} column: "))
                            exists_i_query = f"SELECT count(i_id) FROM ingredients WHERE i_id = {ingredient_new_value}"
                            cur.execute(exists_i_query)
                            if cur.fetchone()[0] == 0:
                                existing_i = False
                            else:
                                print("Please enter an i_id not already in the table")

                    else:
                        ingredient_new_value = input(f"Entry for the {ingredient_cols[counter]} column: ")
                    ingredient_new_values.append(ingredient_new_value)
                    counter += 1
                ingredient_query = f"INSERT INTO ingredients VALUES ({ingredient_new_values[0]},'{ingredient_new_values[1]}','{ingredient_new_values[2]}','{ingredient_new_values[3]}')"
                cur.execute(ingredient_query)
                conn.commit()
                break
            except ValueError:
                print("Please enter a valid id")

def remove(table):
    print(f"You chose to remove an entry from the {table} table")
    if table == "recipes":
        while True:
            try:
                valid_r = False
                while valid_r == False:
                    recipes_remove = int(input("Please type the r_id (recipe id) of the recipe that you want to remove: "))
                    recipe_size_query = f"SELECT COUNT(*) FROM recipes WHERE r_id = {recipes_remove}"
                    cur.execute(recipe_size_query)
                    recipe_sizer = cur.fetchone()
                    recipe_size = recipe_sizer[0]
                    if recipe_size == 0:
                        print("Please enter a valid r_id")
                    else:
                        recipes_remove_query = f"DELETE FROM recipes WHERE r_id = {recipes_remove}"
                        rrequired_remove_query = f"DELETE FROM required WHERE r_id = {recipes_remove}"
                        cur.execute(recipes_remove_query)
                        conn.commit()
                        cur.execute(rrequired_remove_query)
                        conn.commit()
                        valid_r = True
                break
            except ValueError:
                print("Please enter a valid r_id")

    elif table == "required":
        while True:
            try:
                valid_id = False
                while valid_id == False:
                    required_remove_i = int(
                        input("Please type the i_id (ingredient id) of the ingredient you want to remove: "))
                    required_remove_r = int(
                        input("Please type the r_id (recipe id) of the recipe you want to remove an ingredient from: "))
                    recipe_size_query = f"SELECT count(r_id) FROM required WHERE r_id = {required_remove_r}"
                    cur.execute(recipe_size_query)
                    recipe_sizer = cur.fetchone()
                    recipe_size = recipe_sizer[0]

                    ingredients_size_query_r = f"SELECT count(i_id) FROM required WHERE i_id = {recipes_new_value}"
                    cur.execute(ingredients_size_query_r)
                    ingredients_sizer_r = cur.fetchone()
                    ingredients_size_r = ingredients_sizer_r[0]
                    if recipe_size == 0:
                        print("Please enter a valid r_id")
                    elif ingredients_size_r == 0:
                        print("Please enter a valid i_id")
                    else:
                        required_remove_query = f"DELETE FROM required WHERE r_id = {required_remove_r} AND i_id = {required_remove_i}"
                        required_remove_query_r = f"DELETE FROM recipes WHERE r_id = {required_remove_r}"
                        required_remove_query_i = f"DELETE FROM ingredients WHERE i_id = {required_remove_i}"
                        cur.execute(required_remove_query)
                        conn.commit()
                        cur.execute(required_remove_query_r)
                        conn.commit()
                        cur.execute(required_remove_query_i)
                        conn.commit()
                        valid_id = True
                break
            except ValueError:
                print("Please enter a valid r_id and i_id")
    else:
        while True:
            try:
                valid_i = False
                while valid_i == False:
                    ingredients_remove = int(
                        input("Please type the i_id (ingredient id) of the ingredient you want to remove: "))
                    check_query = f"SELECT count(i_id) FROM ingredients WHERE i_id = {ingredients_remove}"
                    cur.execute(check_query)
                    checkers = cur.fetchone()
                    checker = checkers[0]
                    ingredients_size_query = f"SELECT COUNT(*) FROM ingredients"
                    cur.execute(ingredients_size_query)
                    ingredients_sizer = cur.fetchone()
                    ingredients_size = ingredients_sizer[0]
                    if ingredients_remove > ingredients_size:
                        print("Please enter an i_id from the ingredients table")
                    elif checker > 0:
                        print("You can only remove ingredients that do not appear in any recipes. Please try again.")
                    else:
                        ingredients_remove_query = f"DELETE FROM ingredients WHERE i_id = {ingredients_remove}"
                        cur.execute(ingredients_remove_query)
                        conn.commit()
                        valid_i = True
                break
            except ValueError:
                print("Please enter a valid i_id")

def modify():
    valid = False
    while not valid:
        print("\nPlease enter the table and column that you would like to modify")
        table, column = validate_table_col()

        if column in ["r_id", "i_id"]:
            print("You cannot modify primary / foreign key fields")
        else:
            valid = True

    id_type = "i_id"
    if table == "recipes":
        id_type = "r_id"

    if table != "required":
        id_list = cur.execute(f"SELECT {id_type} FROM {table}").fetchall()
        id_list = pd.DataFrame(id_list, columns=["id"])["id"].values.tolist()

        id = validate_id(id_list)

    else:
        r_ids = cur.execute(f"SELECT r_id FROM Recipes").fetchall()
        r_ids = pd.DataFrame(r_ids, columns=["id"])["id"].values.tolist()

        r_id = validate_id(r_ids, "recipe id")

        i_ids = cur.execute(f"SELECT i_id FROM Ingredients").fetchall()
        i_ids = pd.DataFrame(i_ids, columns=["id"])["id"].values.tolist()

        i_id = validate_id(i_ids, "ingredient id")

        record = cur.execute(f"SELECT * FROM Required WHERE r_id == {r_id} AND i_id == {i_id}").fetchone()

        if not record:
            print(f"No record with r_id == {r_id} and i_id == {i_id} exists")
            return

    valid = False
    while not valid:
        print(f"Please enter the new value for {column}")
        new_val = input("=> ")

        if db_schema[table][column] == "text":
            valid = True
        else:
            try:
                new_val = float(new_val)
                valid = True
            except:
                print(f"{column} represents a number, please enter a number")
    
    if table != "required":
        cur.execute(f"UPDATE {table} SET {column} = (?) WHERE {id_type} == {id}", (new_val,))
        conn.commit()
    else:
        cur.execute(f"UPDATE {table} SET {column} = (?) WHERE r_id == {r_id} AND i_id == {i_id}", (new_val,))
        conn.commit()


def validate_id(id_list, type = "id"):
    id = None
    valid = False
    while not valid:
        print(f"\nPlase enter the {type} of the record you would like to modify:")
        try:
            id = float(input("=> "))
        except:
            print("Please enter a number")

        if id in id_list:
            valid = True
        else:
            print("The id you entered is not valid or no record with that id exists, please try another")

    return id

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

def see_ingredients():
    print("You chose to see the ingredients of a recipe")
    exit_i = False
    while exit_i == False:
        while True:
            try:
                r_exists = False
                while r_exists == False:
                    recipe_choice = int(input("Please type the r_id of an existing recipe in the table to see its ingredients: "))
                    r_exists_query = f"SELECT count(*) FROM recipes WHERE r_id = {recipe_choice}"
                    cur.execute(r_exists_query)
                    recipe_checker = cur.fetchone()
                    r_check = recipe_checker[0]
                    if r_check == 0:
                        print("Please enter an existing recipe")
                    else:
                        r_exists = True
                break

            except ValueError:
                print("Please enter a valid r_id")
        recipe_query = f"SELECT r_name FROM recipes WHERE r_id = {recipe_choice}"
        cur.execute(recipe_query)
        recipe_name_line = cur.fetchone()
        recipe_name = recipe_name_line[0]
        ingredients_query = f"SELECT i_name,amount FROM required INNER JOIN ingredients on required.i_id = ingredients.i_id WHERE required.r_id = {recipe_choice}"
        cur.execute(ingredients_query)
        ingredients_checker = cur.fetchall()
        print(f"{recipe_name}:")
        for i in ingredients_checker:
            print(f"{i[1]} {i[0]}")

        good_choice = False
        while good_choice == False:
            print("")
            print("a. See another recipe")
            print("b. exit")
            user_choice = input("=> ")
            if user_choice == "a":
                good_choice = True
            elif user_choice == "b":
                exit_i = True
                good_choice = True
            else:
                print("Please enter a or b")

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

def recipe_from_ingredients():
    ingredients = []

    # Get ingredients from user
    done = False
    while not done:
        print("\nEnter the name of an ingredient or 'done':")
        iname = input("=> ")
        new_ingredient = None

        # Check if user is done entering ingredients
        if iname == "done":
            done = True
        else:
            # Fetch record from table
            new_ingredient = cur.execute("SELECT i_id, i_name FROM ingredients WHERE i_name == (?)", (iname,)).fetchone()
        
        # Add to ingredients, only if record was found
        if new_ingredient:
            ingredients.append(new_ingredient)
        else:
            print("The ingredient you entered was not found")
            
        # print current list of ingredients
        print("So far, you have added:")
        for ingredient in ingredients:
            print(ingredient[1])
    
    # Get list of ingredient ids
    ingredients = pd.DataFrame(ingredients, columns=["i_id", "i_name"])
    i_ids = ingredients["i_id"].values.tolist()

    r_ids = []
    makeable = []
    recipes = cur.execute("SELECT * FROM recipes NATURAL JOIN required").fetchall()

    # Find recipes where all needed ingredients are present
    for recipe in recipes:
        if recipe[0] not in r_ids:
            r_ids.append(recipe[0])
            makeable.append(recipe[1])

        if recipe[-1] not in i_ids:
            try:
                makeable.remove(recipe[1])
            except:
                pass

    # Output recipes that can be made
    print("\nYou can make the following recipes: ")
    for makeable_recipe in makeable:
        print(makeable_recipe)
    
    if len(makeable) == 0:
        print("You can't make any recipes, try entering more ingredients, or restock your pantry!")

    print()

def bar_chart():
    most_used_query = f"SELECT ingredients.i_name, count(required.i_id) as 'appearances' FROM ingredients INNER JOIN required on ingredients.i_id = required.i_id GROUP BY ingredients.i_name ORDER BY appearances DESC LIMIT 10;"
    cur.execute(most_used_query)
    most_used_stuff = cur.fetchall()
    x = []
    y = []
    for i in most_used_stuff:
        x.append(i[0])
        y.append(i[1])
    plt.figure(figsize=(20, 8))
    plt.bar(x, y)
    plt.title("Most used ingredients")
    plt.xlabel("Ingredients")
    plt.ylabel("Number of times used in any recipe")
    plt.show()

def scatter():
    num_servings_query = f"SELECT time, servings FROM recipes;"
    cur.execute(num_servings_query)
    worth_stuff = cur.fetchall()
    x = []
    y = []
    for i in worth_stuff:
        x.append(i[0])
        y.append(i[1])
    plt.scatter(x, y)
    plt.title("How worth it are these recipes: Cook time by number of servings")
    plt.xlabel("Cook Time")
    plt.ylabel("Number of Servings")
    plt.show()

def data_visualization():
    print("You chose to see some data")
    exit_date = False
    while exit_date == False:
        print("a. See number of servings by time")
        print("b. See most used ingredients")
        print("c. Exit")
        data_choice = input("=> ")
        match data_choice:
            case "a":
                scatter()
            case "b":
                bar_chart()
            case "c":
                exit_date = True
            case _:
                print("Please enter a, b, or c")

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
                change_tables()
            case "c":
                stats()
            case "d":
                where()
            case "e":
                see_ingredients()
            case "f":
                recipe_from_ingredients()
            case "g":
                data_visualization()
            case "h":
                print("Logged Out Successfully!")
                quit = True
            case _:
                print("Please enter a, b, c, d, e, f, g or h")

if __name__ == '__main__':
    main()