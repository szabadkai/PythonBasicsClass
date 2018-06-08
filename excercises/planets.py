#! /usr/bin/python3

# Version 0.2

import argparse
import csv


class swstat:
    def __init__(self, csvfile):
        self.file = csvfile

    def __get_value(self, col="", col2="", func="", mode="", terr_filt=""):
        with open(self.file) as f:
            selected = ""
            reader = csv.DictReader(f, quotechar='\'')
            for row in reader:
                # Initialize selected
                if selected == "":
                    selected = row
                try:
                    # Check if terrain filter is disabled, or filter by terrain
                    if (terr_filt == "" or
                        str(row.get("i.terrain").index(terr_filt))):
                        # Simple mode with sorting by one column
                        if mode == "simple":
                            if func == "max":
                                try:
                                    if int(row.get(col)) > int(selected.get(col)):
                                        selected = row
                                # If value cannot be converted to number skip
                                except (ValueError, TypeError):
                                    pass
                            if func == "min":
                                try:
                                    if int(row.get(col)) < int(selected.get(col)):
                                            selected = row
                                # If value cannot be converted to number skip
                                except (ValueError, TypeError):
                                    pass
                except ValueError:
                    pass
                # Advanced mode sorting by two columns
                if mode == "adv":
                    if func == "max":
                        try:
                            if (((int(row.get(col)) /
                                (int(row.get(col2))))) >
                                ((int(selected.get(col)) /
                                    (int(selected.get(col2)))))):
                                    selected = row
                        # If value cannot be converted to number or is zero skip
                        except (ZeroDivisionError, ValueError):
                            pass
                    if func == "min":
                        try:
                            if (((int(row.get(col)) /
                                (int(row.get(col2))))) <
                                ((int(selected.get(col)) /
                                    (int(selected.get(col2)))))):
                                    selected = row
                        # If value cannot be converted to number or is zero skip
                        except (ZeroDivisionError, ValueError):
                            pass

        return selected

    def highest_population(self):
        res = self.__get_value(mode="simple", col="population", func="max")
        print(f"The planet {res.get('name')} has the highest population: {res.get('population')}")

    def highest_water(self):
        res = self.__get_value(mode="simple", col="surface_water", func="max")
        print(f"The planet {res.get('name')} has the highest ratio of water: {res.get('surface_water')}")

    def population_density(self):
        res = self.__get_value(mode="adv", col="population", col2="diameter", func="max")
        print("The planet " + res.get('name') + "has the highest population " +
              "density: " + str((int(res.get('population')) / int(res.get('diameter')))))

        res = self.__get_value(mode="adv", col="population", col2="diameter", func="min")
        print("The planet " + res.get('name') + "has the lowest population " +
              "density: " + str((int(res.get('population')) / int(res.get('diameter')))))

    def most_grasslands(self):
        res = self.__get_value(mode="simple", col="population", func="max",
                               terr_filt="grasslands")
        print(f"The planet {res.get('name')} has the most grasslands: {res.get('diameter')}")

#        print(self.__get_value(mode="simple", col="population", func="min",
#                               terr_filt="grasslands"))


def main():
    parser = argparse.ArgumentParser(description="""This program prints
                                     statistics about planets.""")
    parser.add_argument("-p", "--population", help="""Print highest
                        population.""", action="store_true")
    parser.add_argument("-w", "--water", help="""Print highest ratio of
                        water.""", action="store_true")
    parser.add_argument("-d", "--density", help="""Print highest and lowest
                        population density.""", action="store_true")
    parser.add_argument("-g", "--grasslands", help="""Print most
                        grasslands.""", action="store_true")
    parser.add_argument("-f", "--file", help="""Filename to read planet
                        data from.""", required=True)
    args = parser.parse_args()

    # Instantiate and initialize swstat class
    planets = swstat(args.file)

    # If
    if args.population:
#        print("This is the population function")
        planets.highest_population()

    if args.water:
#        print("This is the water function")
        planets.highest_water()

    if args.density:
#        print("This is the population density function")
        planets.population_density()

    if args.grasslands:
#        print("This is the grassland function")
        planets.most_grasslands()


if __name__ == "__main__":
    main()
