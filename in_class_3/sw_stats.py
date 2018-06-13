import csv
import json
import math

def try_or_NAN(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return "NAN"
    return wrapper

class Planet:
    allowed_keys = ['name', 'region', 'population', 'gravity', 'orbital_period', 'terrain', 'diameter',
                    'surface_water']

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __init__(self, name, region, population, gravity, orbital_period, terrain, diameter, surface_water):
        self.name = name
        self.region = region
        self.population = int(population) if population != "unknown" else "NAN"
        self.gravity = gravity
        self.orbital_period = orbital_period
        self.terrain = terrain.split(", ")
        self.diameter = int(diameter) if diameter != "unknown" else "NAN"
        self.surface_water = float(surface_water) if surface_water != "unknown" else "NAN"

    def from_dict(self, d):
        return Planet(**{k:d[k] for k in self.allowed_keys})

    @property
    @try_or_NAN
    def surface(self):
        return 4*(self.diameter/2)**2*math.pi


    @property
    @try_or_NAN
    def population_density(self):
        return self.population/self.surface


    def __repr__(self):
        return json.dumps({k:self[k] for k in self.allowed_keys})

class PlanetStat:
    def __init__(self, fh):
        self._planets = [Planet(**planet) for planet in csv.DictReader(fh, delimiter=",", quotechar="'")]

    def __iter__(self):
        return iter(self._planets)

    def highest_population(self):
        return self.highest("population")

    def highest_surface_water(self):
        return self.highest("surface_water")

    def highest(self, arg):
        return max([planet for planet in self if planet[arg] != "NAN"], key=lambda x:x.__getattribute__(arg))


if __name__ == "__main__":
    with open("sw_planets_2nd_edition.csv.txt") as csv_file:
        stats= PlanetStat(csv_file)
        print(
            stats.highest_population(),
            stats.highest_surface_water(), sep="\n"
        )
