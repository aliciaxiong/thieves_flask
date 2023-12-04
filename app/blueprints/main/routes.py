from app.blueprints.main import main
from flask import render_template, request, session, url_for, redirect
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
            if 'team' not in session: 
                session['team'] = []
            session['team'].append(poke_dict)
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

#Pokemon Team Page 
@main.route('/team')
@login_required
def team():
    team = session.get('team', [])
    return render_template('team.html', team=team)

#Adding a Pokemon to the Team
@main.route('/add', methods=['POST'])
@login_required
def add():
    pokemon_name = request.form.get('pokemon_name')
    print(f"adding pokemon: {pokemon_name}")
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(url)

    if not response.ok:
        return render_template('invalid.html')
    
    data = response.json()
    poke_dict = pokemon_data(data)

    if 'team' not in session: 
        session['team'] = []

    session['team'].append(poke_dict)
    return redirect(url_for('main.team'))


#Pokemon Battle Page 
@main.route('/battle')
@login_required
def battle():
    return render_template('battle.html')

#Removing a pokemon from the team 
@main.route('/remove', methods=['POST'])
@login_required
def remove():
    pokemon_name = request.form.get('pokemon_name')
    team = session.get('team', [])
    for pokemon in team: 
        if pokemon['pokemon_name'] == pokemon_name: 
            team.remove(pokemon)
            session['team'] = team
            break
    return redirect(url_for('main.team'))