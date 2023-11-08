from flask import Flask, render_template, request
import requests

app = Flask(__name__)

#LOGIN PAGE 
@app.route('/user/login', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST': 
            return "You have successfully logged in Pokemon Trainer"
    else: 
        return render_template('login.html')

#POKEDEX PAGE  
@app.route('/pokedex', methods=['GET', 'POST'])
def get_pokemon_data():
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        try: 
            pokemon_data = response.json()
            all_pokemon = get_pokemon_data(pokemon_data)
            return render_template('pokedex.html', all_pokemon=all_pokemon)
        except:
            return 'Enter a Valid Pokemon'
    else: 
        return render_template('pokedex.html')

def pokemon_data(data): 
    old_pokemon_data = []
    for poke in data: 
        poke_dict = {
            'pokemon_name': poke['forms'][0]['name'],
            'ability_name': poke['abilities'][0]['ability']['name'], 
            'base_experience': poke['base_experience'],
            'attack_base_stat': poke['stats'][1]['base_stat'],
            'hp_base_stat': poke['stats'][0]['base_stat'],  
            'defense_base_stat': poke['stats'][2]['base_stat'],  
            'sprite': poke['sprites']['front_shiny'] 
        }
        old_pokemon_data.append(poke_dict)
    return old_pokemon_data
