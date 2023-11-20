from flask import request, render_template, redirect, url_for, flash
import requests
from app import app 
from app.forms import LoginForm, SignupForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


#HOME PAGE
@app.route('/home')
def home(): 
    return render_template('home.html')

#LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Welcome, {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            return 'Please try again, email or password is invalid.'
    else:
            return render_template('login.html', form=form)

#SIGNUP PAGE
@app.route('/signup', methods=['GET', 'POST'])
def route(): 
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        user = User(first_name, last_name, email, password)

        db.session.add(user)
        db.session.commit()

        flash(f' Thank you {first_name}!', 'sucess')
        return redirect(url_for('login'))

    else: 
        return render_template('signup.html', form=form)

#LOGOUT PAGE 
@app.route('/logout') 
@login_required
def logout():
    flash('Successfully logged out, see you soon trainer!', 'warning')
    logout_user()
    return redirect(url_for('login'))

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