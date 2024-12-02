import sqlite3

conn = sqlite3.connect("social_media.db")
cur = conn.cursor()


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
            case "b":
            case "c":
            case "d":
            case "e":
            case "f":
            case "g":
            case "h":
                print("Logged Out Successfully!")
                quit = True
            case _:
                print("Please enter a, b, c, d, e, f, g or h")


if __name__ == '__main__':
    main()