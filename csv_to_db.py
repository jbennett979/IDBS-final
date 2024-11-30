import sqlite3
import pandas as pd

df_ingredients = pd.read_csv('ingredients.csv')
df_recipes = pd.read_csv('recipes.csv')
df_required = pd.read_csv('required.csv')

conn = sqlite3.connect("recipes_final.db")
cur = conn.cursor()

ingredients_table = "CREATE TABLE IF NOT EXISTS ingredients(i_id INTEGER PRIMARY KEY, i_name TEXT NOT NULL, flavor TEXT, type TEXT);"

recipes_table = "CREATE TABLE IF NOT EXISTS recipes(r_id PRIMARY KEY, r_name TEXT, description TEXT, rating NUMERIC, time INTEGER, servings INTEGER);"

required_table = "CREATE TABLE IF NOT EXISTS required(r_id INTEGER, amount TEXT, i_id INTEGER);"

cur.execute(ingredients_table)
cur.execute(recipes_table)
cur.execute(required_table)

df_ingredients.to_sql('ingredients', conn, if_exists='replace', index = False)
df_recipes.to_sql('recipes', conn, if_exists='replace', index = False)
df_required.to_sql('required', conn, if_exists='replace', index = False)



