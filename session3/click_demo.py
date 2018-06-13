import click
from sw_planets_stats import SwDataSet
import json

@click.command()
@click.option('--file', help='csv file containing our astronomical data.', type=str, default=None)
@click.option('--highest', help='Specify which attribute you want the highest from', default=None)
@click.option('--lowest', help='Specify which attribute you want the lowest from', default=None)
@click.option('--as_json', help='Outputs json formated data', is_flag=True)
def hello(file, highest, lowest, as_json):
    if file is None:
        print("Please Provide a file to open")
        return
    with open(file) as datafile:
        data_set = SwDataSet(datafile)
        if highest:
            planet=data_set.highest(lambda x: x.__getattribute__(highest))
            if as_json:
                print( json.dumps(planet.as_dict()) )
            else:
                print( "The highest {0} is on:\n{1}".format(highest, planet))

        elif lowest:
            print( "The lowest {0} is on:\n{1}".format(lowest, data_set.highest(lambda x: x.__getattribute__(lowest))))


if __name__ == '__main__':
    hello()