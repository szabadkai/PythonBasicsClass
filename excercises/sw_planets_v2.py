import sys
import math
import argparse

def init_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--high_pop', help='highest population', action='store_true')
    group.add_argument('-r', '--high_ratio_water', help='highest ratio of water', action='store_true')
    group.add_argument('-d', '--high_low_pop', help='highest and lowest population density', action='store_true')
    group.add_argument('-g', '--grasslands', help='region with the most grasslands', action='store_true')
    parser.add_argument('filename')
    if len(sys.argv) != 3:
        print(parser.print_help())
    return vars(parser.parse_args())


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


class process_data():
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.header = next(self.file_handler).strip().split(',')

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self._proces_by_line()
        except IndexError:
            raise StopIteration
        return result

    def _get_data_dict(self, line):
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
        return {k: v for k,v in zip(self.header, list)}

    def _proces_by_line(self):
        next_line = next(self.file_handler)
        data = (self._get_data_dict(next_line))
        return data


def main():
    args = init_args()
    attr = ([k for k,v in args.items() if k != 'filename' and v==True ][0])
    with open(args['filename'], 'r') as f:
        swp = sw_planet()
        processor = process_data(f)
        for data in processor:
            getattr(swp, attr)(data)

    print(getattr(swp, 'print_' + attr)())


if __name__ == "__main__":
    main()
