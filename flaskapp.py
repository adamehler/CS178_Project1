from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import creds
from dbCode import * #helper functions from dbCode



app = Flask(__name__)
app.secret_key = 'your_secret_key' #This came from the example flaskapp.py in class
#Home page

@app.route("/")
def home():
    #Get the top 20 most common official languages
    languages = get_most_pop_off_lang()
    #Utilize the template to render the page
    return render_template("official_languages.html", results=languages)

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    countries = get_all_country_names()
    
    if request.method == 'POST':
        username = request.form['username']
        selected_countries = request.form.getlist('countriesVisited')  # get multiple selected options
        user_add(username, selected_countries)
        flash('User added successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('add_user.html', countries=countries)



@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    users = get_all_users()
    if request.method == 'POST':
        name = request.form['name']
        user_delete(name)
        flash('User deleted successfully!', 'warning')
        return redirect(url_for('home'))
    else:
        return render_template('delete_user.html', users=users)


@app.route('/user-read', methods=['GET', 'POST'])
def user_read_route():
    users = get_all_users()
    if request.method == 'POST':
        username = request.form['username']
        countries = user_read(username)

        if not countries:
            flash(f"No countries found for user '{username}'", 'danger')
            return redirect(url_for('user_read_route'))

        placeholders = ', '.join(['%s'] * len(countries))
        query = f"""
            SELECT city.Name, city.CountryCode 
            FROM city 
            JOIN country ON city.CountryCode = country.Code 
            WHERE country.Name IN ({placeholders})
        """
        cities = execute_query(query, countries)
        return render_template('user_read.html', username=username, cities=cities)
    
    return render_template('get_user.html', users=users)


if __name__ == '__main__': #Came from the examples so prob important
    app.run(host='0.0.0.0', port=8080, debug=True)