from app.blueprints.main import main
from flask import render_template, request
from flask_login import login_required
import requests

#HOME PAGE
@main.route('/home')
def home(): 
    return render_template('home.html')

#POKEDEX PAGE  
@main.route('/pokedex', methods=['GET', 'POST'])
@login_required
def get_pokemon_data():
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        print(pokemon_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        try: 
            data = response.json()
            poke_dict = pokemon_data(data)
            return render_template('pokedex.html', poke_dict=poke_dict)
        except:
            return render_template('invalid.html')
    else: 
        return render_template('pokedex.html')

def pokemon_data(data): 
    poke_dict = {
            'pokemon_name': data['forms'][0]['name'],
            'ability_name': data['abilities'][0]['ability']['name'], 
            'base_experience': data['base_experience'],
            'attack_base_stat': data['stats'][1]['base_stat'],
            'hp_base_stat': data['stats'][0]['base_stat'],  
            'defense_base_stat': data['stats'][2]['base_stat'],  
            'sprite': data['sprites']['front_default'] 
    }
    return poke_dict