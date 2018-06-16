import sys
import math

def help():
    msg = """
Options:
    -p  highest population
    -r  highest ratio of water
    -d  highest and lowest population density
    -g  region with the most grasslands
"""

    print('usage: %s {option} file' % sys.argv[0])
    print(msg)
    sys.exit(1)


class sw_planet():
    def __init__(self):
        self.planet = ''
        self.region = ''
        self.population = 0
        self.surface_water = 0
        self.density_low = 100000
        self.density_high = 0
        self.planet_density_high = ''
        self.planet_density_low = ''
        self.mainland = 0

    def high_pop(self,data):
        try:
            new_pop = int(data['population'])
            new_planet = data['name']
            if  new_pop > self.population:
                self.population = new_pop
                self.planet = new_planet
        except:
            pass

    def high_ratio_water(self, data):
        try:
            new_surface_water = int(data['surface_water'])
            new_planet = data['name']
            if new_surface_water > self.surface_water:
                self.surface_water = new_surface_water
                self.planet = new_planet
        except:
            pass

    def _get_mainland(self,data):
            try:
                new_diameter = int(data['diameter'])
                new_surface_water = int(data['surface_water'])
                surface = 4 * math.pi * (new_diameter/2)**2
                return surface * ( 1 - new_surface_water/100)
            except:
                return None

    def _get_density(self,data):
        try:
            mainland = self._get_mainland(data)
            if mainland:
                new_pop = int(data['population'])
                return new_pop / mainland
            else:
                return None
        except:
            return None

    def high_low_pop(self, data):
        try:
            new_density = self._get_density(data)
            if new_density:
                if new_density > self.density_high:
                    self.density_high = new_density
                    self.planet_density_high = data['name']
                elif new_density < self.density_low:
                    self.density_low = new_density
                    self.planet_density_low = data['name']
        except:
            pass

    def grasslands(self, data):
        pattern = 'grass'
        grass_found = len(''.join(w for w in data['i.terrain'] if pattern in w))
        if grass_found > 0:
            new_mainland = self._get_mainland(data)
            if new_mainland and new_mainland > self.mainland:
                self.mainland = new_mainland
                self.region = data['region']

    def print_grasslands(self):
        return f"{self.region}"

    def print_high_low_pop(self):
        return f"{self.planet_density_high}: {self.density_high} / {self.planet_density_low}: {self.density_low}"

    def print_high_pop(self):
        return f"{self.planet}: {self.population}"

    def print_high_ratio_water(self):
        return f"{self.planet}: {self.surface_water}"


def get_data_dict(header, line):
    list = []
    field = []
    inside_list = False
    for char in line:
        if char == "'":
            inside_list = not inside_list
        if inside_list:
            field.append(char)
        else:
            if char == ',' or char == '\n':
                if ',' in field:
                    list.append(''.join(field).strip("'").split(', '))
                else:
                    list.append(''.join(field))
                field = []
            else:
                field.append(char)
    return {k: v for k,v in zip(header, list)}


def calculate(filename,attr):
    swp = sw_planet()
    with open(filename) as f:
        header = next(f).strip().split(',')
        for line in f.readlines():
            data = (get_data_dict(header,line))
            getattr(swp, attr)(data)
    print(getattr(swp, 'print_' + attr)())


def main():
    if len(sys.argv) != 3:
        help()

    option = sys.argv[1]
    filename = sys.argv[2]

    if option == '-p':
        calculate(filename, 'high_pop')
    elif option == '-r':
        calculate(filename, 'high_ratio_water')
    elif option == '-d':
        calculate(filename, 'high_low_pop')
    elif option == '-g':
        calculate(filename, 'grasslands')
    else:
        print('unknown option: ' + option)
        sys.exit(1)


if __name__ == "__main__":
    main()
