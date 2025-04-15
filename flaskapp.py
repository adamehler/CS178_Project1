from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import creds
from flask import jsonify
from dbCode import * #helper functions from dbCode



app = Flask(__name__)
app.secret_key = 'your_secret_key' #This came from the example flaskapp.py in class
#Home page

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/languages")
def languages():
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


@app.route('/get-user-countries', methods=['POST'])
def get_user_countries():
    username = request.form.get('username')
    if not username:
        return jsonify({'error': 'No username provided'}), 400

    current_countries = user_read(username)
    all_countries = get_all_country_names()
    available_countries = [c for c in all_countries if c not in current_countries]

    return jsonify({
        'current_countries': current_countries,
        'available_countries': available_countries
    })



@app.route('/user-read', methods=['GET', 'POST'])
def user_read_route():
    users = get_all_users()  # Get the list of users

    if request.method == 'POST':
        username = request.form['username']  # Get the username from the form
        countries = user_read(username)  # Get countries for the selected user

        if not countries:
            flash(f"No countries found for user '{username}'", 'danger')
            return redirect(url_for('user_read_route'))  # Redirect if no countries are found

        placeholders = ', '.join(['%s'] * len(countries))  # Prepare placeholders for SQL query
        query = f"""
            SELECT city.Name AS city_name, 
             city.CountryCode AS country_code, 
             city.Population AS population,
             city.District AS district,
             country.Name AS country_name,
             GROUP_CONCAT(countrylanguage.Language) AS languages
             FROM city 
             JOIN country ON city.CountryCode = country.Code 
             LEFT JOIN countrylanguage ON country.Code = countrylanguage.CountryCode
             WHERE country.Name IN ({placeholders})
             GROUP BY city.Name, city.CountryCode, city.Population, city.District, country.Name

        """
        cities = execute_query(query, countries)  # Execute the query

        return render_template('user_read.html', username=username, cities=cities)  # Render cities page

    # If the method is GET, render the user selection page
    return render_template('get_user.html', users=users)


@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    users = get_all_users()

    if request.method == 'POST':
        username = request.form['username']
        updated_list = request.form.getlist('updatedCountries')
        table.put_item(Item={'User': username, 'CountriesVisited': updated_list})
        return render_template('update_user.html', users=users, success=True)

    return render_template('update_user.html', users=users)




if __name__ == '__main__': #Came from the examples so prob important
    app.run(host='0.0.0.0', port=8080, debug=True)