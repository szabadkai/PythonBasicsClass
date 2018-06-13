import csv
import math


def try_or_NAN(f):
    def func_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return "NAN"

    return func_wrapper


class SwDataSet:
    def __init__(self, datafile):
        self.planets = [Planet.from_dict(d) for d in csv.DictReader(datafile, delimiter=',', quotechar="'")]

    def __iter__(self):
        return iter(self.planets)

    def __getitem__(self, item):
        for p in self:
            if p.name.lower() == item.lower():
                return p
        raise KeyError(f"no such planet: {item}")

    def highest(self, f):
        return max([p for p in self if not isinstance(f(p), str)], key=lambda x: f(x))

    def lowest(self, f):
        return min([p for p in self if not isinstance(f(p), str)], key=lambda x: f(x))


class Planet:
    allowed_keys = ['name', 'region', 'population', 'gravity', 'orbital_period', 'terrain', 'diameter', 'surface_water']

    def __init__(self, name, region, population, gravity, orbital_period, terrain, diameter, surface_water):
        self.name = name
        self.region = region
        self.population = int(population) if population != "unknown" else "NAN"
        self.gravity = gravity
        self.orbital_period = orbital_period
        self.terrain = terrain.split(", ")
        self.diameter = int(diameter) if diameter != "unknown" else "NAN"
        self.surface_water = float(surface_water) if surface_water != "unknown" else "NAN"


    def __iter__(self):
        return iter([ (k, self.__getattribute__(k)) for k in Planet.allowed_keys])

    @property
    @try_or_NAN
    def surface(self):
        return 4 * (self.diameter / 2) ** 2 * math.pi

    @property
    @try_or_NAN
    def population_density(self):
        return self.population / (100 - self.surface_water) * self.surface

    @staticmethod
    def from_dict(d):
        return Planet(**{key: d[key] for key in Planet.allowed_keys})

    def __repr__(self):
        return "\n".join([f"{k}: {self.__getattribute__(k)}" for k in self.allowed_keys])


if __name__ == "__main__":
    with open("sw_planets_2nd_edition.csv.txt") as datafile:
        data_set = SwDataSet(datafile)
        print(data_set.highest(lambda x: x.population))
        print()
        print(data_set.highest(lambda x: x.surface_water))
        print()
        print(data_set.highest(lambda x: x.population_density))
