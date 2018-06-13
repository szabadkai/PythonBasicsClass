import click
import sw_stats


@click.command()
@click.option("--file", help="CSV file containing astronomical data")
@click.option("--highest", help="get planet with highes attribute")
@click.option("--dryrun", help="dont print, just open", is_flag=True)
def demo(file, highest, dryrun):
    if not file:
        print ("Please provide file to work with")
        return
    with open(file) as csv_file:
        stats= sw_stats.PlanetStat(csv_file)
        if dryrun:
            return 
        print(
            stats.highest(highest)
        )


if __name__ == "__main__":
    demo()