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
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        countriesVisited = request.form['countriesVisited']
        user_add(username, countriesVisited) #use dbCode add to add to NoSQL

        
        # Process the data (e.g., add it to a database)
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/delete-user',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        user_delete(name)
        flash('User deleted successfully!', 'warning')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/user_read', methods=['GET', 'POST']) #From CHATGPT
def visited_cities():
    if request.method == 'POST':
        username = request.form['username']
        countries = user_read(username)

        if not countries:
            flash(f"No countries found for user '{username}'", 'danger')
            return redirect(url_for('home'))

        # Build SQL query
        placeholders = ','.join(['%s'] * len(countries)) #Chat GPTs solution to getting list of countries
        query = f"SELECT * FROM city WHERE CountryCode IN (SELECT Code FROM country WHERE Name IN ({placeholders}))"
        
        # Execute query
        results = execute_query(query, countries)

        return render_template('user_read.html', username=username, cities=results)

    return render_template('get_user.html')  # This will have the form to enter username


if __name__ == '__main__': #Came from the examples so prob important
    app.run(host='0.0.0.0', port=8080, debug=True)