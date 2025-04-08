from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import creds
from dbCode import * #helper functions from dbCode


app = Flask(__name__)
app.secret_key = 'your_secret_key' #This came from the example flaskapp.py in class
#Home page

@app.route("/")
def index():
    #Get the top 20 most common official languages
    languages = get_most_pop_off_lang()
    #Utilize the template to render the page
    return render_template("official_languages.html", results=languages)

if __name__ == '__main__': #Came from the examples so prob important
    app.run(host='0.0.0.0', port=8080, debug=True)