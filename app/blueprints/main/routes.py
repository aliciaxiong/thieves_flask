from app.blueprints.main import main
from flask import render_template, request, session, url_for, redirect, flash
from flask_login import login_required, current_user
import requests
from app.models import User

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

            user_team = f'team_{current_user.id}'
            if user_team not in session:
                session[user_team] = []

            session[user_team].append(poke_dict)
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
    user_team = f'team_{current_user.id}'
    team = session.get(user_team, [])
    return render_template('team.html', team=team)

#Adding a Pokemon to the Team
@main.route('/add', methods=['POST'])
@login_required
def add():
    pokemon_name = request.form.get('pokemon_name')
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poke_dict = pokemon_data(data)
        user_team = f'team_{current_user.id}'

        if user_team not in session:
            session[user_team] = []

        if len(session[user_team]) >= 6:
            return "Team is full"
        session[user_team].append(poke_dict)
        session.modified = True
        return redirect(url_for('main.team'))
    else:
        return "Error: Pokemon not found"

#Removing a pokemon from the team 
@main.route('/remove', methods=['POST'])
@login_required
def remove():
    pokemon_name = request.form.get('pokemon_name')
    user_team = f'team_{current_user.id}'
    session[user_team] = [pokemon for pokemon in session[user_team] if pokemon['pokemon_name'] != pokemon_name]
    session.modified = True
    return redirect(url_for('main.team'))


#Creating a route to be able to search for another user to battle: 
@main.route('/search_user', methods=['GET', 'POST'])
@login_required
def search_user():
    user = None
    pokemon_team = None
    if request.method == 'POST':
        id = request.form.get('userid')
        user = User.query.get(id)
        if user: 
            pokemon_team_k = f'team+{user.id}'
            pokemon_team = session.get(pokemon_team_k, [])
            session['opp_id'] = user.id
        else:
            flash('User not found')
    return render_template('search_user.html', user=user, pokemon_team=pokemon_team)

#Pokemon Battle Page 
@main.route('/battle', methods=['POST'])
@login_required
def battle():
    # Retrieve the teams from the session
    user_team_key = f'team_{current_user.id}'
    user_team = session.get(user_team_key, [])
    opp_id = session.get('opp_id')
    opp_team_key = f'team_{opp_id}'
    opp_team = session.get(opp_team_key, [])

    # Calculate the total stats for each team
    user_total_stats = sum(pokemon['base_experience'] for pokemon in user_team)
    opp_total_stats = sum(pokemon['base_experience'] for pokemon in opp_team)

    # Determine the winner
    if opp_total_stats > user_total_stats:
        winner = 'Opponent'
    elif user_total_stats > opp_total_stats:
        winner = 'You'
    else:
        winner = 'Draw'

    # Render the battle results
    return render_template('battle.html', winner=winner)