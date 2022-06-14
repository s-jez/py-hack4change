import json
from flask import Flask, redirect, url_for, render_template, request
import requests
app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
@app.route('/index')
def index():
    r = requests.get("https://api.v2.emissions-api.org/api/v2/products.json")
    productsDict = json.loads(r.text)
    return render_template("index.html", name='Stanislaw', products=productsDict)
@app.route('/<name>')
def welcome(name):
    return f'Hello <b>{name}</b> 👋!'
@app.route('/anonim')
def anonim():
    return redirect(url_for("welcome", name='Guest'))
@app.route('/articles')
def articles():
    articles = [
        {
            'author': {'nickname': 'Schneider'},
            'title': 'Global warming: are we entering the greenhouse century',
            'link': 'https://www.osti.gov/biblio/6761224'
        },
        {
            'author': {'nickname': 'A. Berger'},
            'title': 'The greenhouse effect',
            'link': 'https://link.springer.com/article/10.1007/BF01904998'
        }
    ]
    return render_template("articles.html", title='Articles of Global Warming', articles=articles)
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        req = request.form
        missing = list()
        for key, value in req.items():
            if value == '':
                missing.append(key)
        
        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("user.html", feedback=feedback)
        username = request.form['username']
        age = request.form['age']
        # flash(f'Hi {user} ! 🔥  You are here! Go Crazy 🔥 ')
        return render_template("user.html", user=username, age=age)
    else:   
        return render_template("user.html")
@app.route('/calculator', methods=['GET', 'POST'])
@app.route('/calculator', methods=['GET', 'POST'])
def calculate_footprint():
    if request.method == 'POST':
        if 'time' in request.form and 'power' in request.form:
            power = int(request.form['power'])
            time = int(request.form['time'])
            footprint = round((758 * power/1000 * time/60 ) / 1000, 2)
            return render_template("calculator.html", footprint=footprint)
    else:
        return render_template("calculator.html")
@app.route('/bmi', methods=['GET', 'POST'])
def calculate_bmi():
    if request.method == 'POST':
        if 'height' in request.form and 'weight' in request.form:
            height = int(request.form['height'])
            weight = int(request.form['weight'])
            bmi = round(weight / (height * 1.65) * 100, 2)
        return render_template("bmi.html", bmi=bmi)
    return render_template("bmi.html")

FOOTPRINT_PER_COUTRY = {
    "PL" : 758,
    "DE": 485,
    "FR": 57.3,
    "ES": 167,
    "UK": 233,
    "IN": 852,
    "CN": 549,
    "US": 386,
}
@app.route('/calculate', methods=['GET', 'POST'])
def calc_footprint():
    if request.method == 'POST':
        if 'time' in request.form and 'power' in request.form:
            power = float(request.form['power'])
            time = float(request.form['time'])
            country = request.form['country']

            footprint = FOOTPRINT_PER_COUTRY[country] * power/100 * time/60
            resFootprint = round(footprint / 10000, 2);

            return render_template("calculate.html", footprint=resFootprint)
    else:
        return render_template("calculate.html")
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        if 'country' in request.form and 'city' in request.form:
            country = request.form['country']
            city = request.form['city']
            req = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + city + ", ", ","+country+"&appid="+"68021e0d3fd79384bad496810806bfda&units=metric")
            weatherDict = json.loads(req.text)
            return render_template("weather.html", temperature=weatherDict['main']['temp'], tempMin=weatherDict['main']['temp_min'], tempMax=weatherDict['main']['temp_max'])
    else:
        return render_template("weather.html")
if __name__ == "__main__":
  app.run()