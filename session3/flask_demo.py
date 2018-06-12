from flask import Flask, request
from sw_planets_stats import SwDataSet
import json

app = Flask(__name__)
app.debug = True  # Enable reloader and debugger

planetstats =  SwDataSet(open('sw_planets_2nd_edition.csv.txt'))


@app.route('/')
def main():
    return 'Hello, this is sw planets api!'

@app.route('/planets')
def planets():
    return json.dumps([planet.name for planet in planetstats])

@app.route('/highest/<attr>')
def highest(attr):
    return json.dumps(
         planetstats.highest(lambda x:x.__getattribute__(attr)).as_dict()
    )

@app.route('/<planet>/<attr>')
def planet_stat_access(planet, attr):
    return json.dumps({ attr: planetstats[planet].__getattribute__(attr)})

@app.route('/<planet>')
def planet_stat(planet):
    return json.dumps(planetstats[planet].as_dict())

@app.route('/planet/search', methods=['POST'])
def search():
    params = request.json
    return json.dumps([planet.as_dict() for planet in planetstats if filter_planet(planet, params)])

def filter_planet(planet, params):
    d = planet.as_dict()
    for k in params:
        if k in d and params[k] == d[k]:
            continue
        else:
            return False
    return True


if __name__ == '__main__':
    app.run(port=5001)