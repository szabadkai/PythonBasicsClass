from flask import Flask, request
from sw_stats import PlanetStat
app = Flask(__name__)
app.debug=True

planets = PlanetStat(open("sw_planets_2nd_edition.csv.txt"))

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/planets')
def get_planets():
    return "<br>".join([p.name for p in planets])\

@app.route('/planet/<name>')
def get_planet(name):
    return str([p for p in planets if p.name == name][0])

@app.route('/highest/<attr>')
def get_planet_attr(attr):
    return str(planets.highest(attr))


if __name__ == "__main__":
    app.run(port=5001)