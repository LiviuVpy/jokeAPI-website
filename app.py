from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
current_year = datetime.datetime.now().year

app = Flask(__name__)
app.secret_key = os.environ['APP_KEY']

@app.route("/")
def index():
    return render_template('index.html', year=current_year)

@app.route('/joke', methods=['POST'])
def joke():
    selected_categories = request.form.getlist('checkbox')
    selected_flags = request.form.getlist('checkboxflag')
    selected_language = request.form.get('language')
    selected_joke_type = request.form.get('inlineRadioOptions')

    categories = ','.join(selected_categories)
    flags = ','.join(selected_flags)
    
    joke_response = requests.get(f"https://v2.jokeapi.dev/joke/{categories}?lang={selected_language}&blacklistFlags={flags}&type={selected_joke_type}")
    try:
        data = joke_response.json()
    except Exception:
        flash("No matching joke found")
        return redirect(url_for('index'))
    else:
        if 'joke' in data:
            joke_text = data['joke']
        elif 'setup' in data:
            joke_text = data['setup'] + ' ' + data['delivery']
        elif 'message' in data:
            flash("No matching joke found")
            return redirect(url_for('index'))
        category = data['category']
        return render_template('joke.html', 
                            year=current_year,
                            joke_text=joke_text,
                            category=category)
    

@app.route('/about')
def about():
    return render_template('about.html', year=current_year)


if __name__ == '__main__':
    app.run(debug=True)