from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
from dotenv import load_dotenv

if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()

app = Flask(__name__)

SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

if not SPOONACULAR_API_KEY:
    raise ValueError("No API key found.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        ingredients = request.form.get('ingredients', '')
        if not ingredients:
            return redirect(url_for('index'))  # Redirect back to index if no ingredients

        response = requests.get(
            "https://api.spoonacular.com/recipes/findByIngredients",
            params={
                "apiKey": SPOONACULAR_API_KEY,
                "ingredients": ingredients,
                "number": 20,
                "ranking": 2,
                "ignorePantry": True
            }
        )
        
        if response.status_code != 200:
            # Handle error response from the API
            return render_template('recipes.html', recipes=[], error="Failed to fetch recipes.")

        all_recipes = response.json()
        recipes = []

        for recipe in all_recipes:
            recipes.append(recipe)

        return render_template('recipes.html', recipes=recipes)
    
    # Handle GET request
    return render_template('recipes.html', recipes=[])

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    response = requests.get(
        f"https://api.spoonacular.com/recipes/{recipe_id}/information",
        params={
            "apiKey": SPOONACULAR_API_KEY
        }
    )
    
    if response.status_code != 200:
        # Handle error response from the API
        return render_template('recipe_detail.html', recipe=None, error="Failed to fetch recipe details.")

    recipe = response.json()
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/get_ingredients')
def autocomplete_ingredients():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])
    
    response = requests.get(
        "https://api.spoonacular.com/food/ingredients/autocomplete",
        params={
            "apiKey": SPOONACULAR_API_KEY,
            "query": query,
            "number": 5
        }
    )
    
    if response.status_code != 200:
        return jsonify([])  # Return an empty list on error

    suggestions = [item['name'] for item in response.json()]
    return jsonify(suggestions)