from flask import Flask, render_template, request
import requests

app = Flask(__name__)

#HOME PAGE 

#POKEDEX PAGE  
@app.route('/pokedex', methods=['GET', 'POST'])
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
            return 'Enter a Valid Pokemon'
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
            'sprite': data['sprites']['front_shiny'] 
        }
    return poke_dict
