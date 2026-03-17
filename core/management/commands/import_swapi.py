from django.core.management import BaseCommand
from django.db import transaction

from core.services import import_planets, import_films, import_species, import_starships, import_vehicles, \
    import_characters


class Command(BaseCommand):
    help= "Import swapi urls"

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("Importing planets")
        import_planets()

        self.stdout.write("Importing films")
        import_films()

        self.stdout.write("Importing species")
        import_species()

        self.stdout.write("Importing starships")
        import_starships()

        self.stdout.write("Importing vehicles")
        import_vehicles()

        self.stdout.write("Importing characters")
        import_characters()

        self.stdout.write("All finished!!!")