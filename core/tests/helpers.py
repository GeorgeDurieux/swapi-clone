from django.utils import timezone
from core.models import Planet, Film, Species, Starship, Vehicle, Character


class DataHelperMixin:
    def planet_data(self, **kwargs):
        data = {
            "name": "Tatooine",
            "diameter": "10465",
            "rotation_period": "23",
            "orbital_period": "304",
            "gravity": "1 standard",
            "population": "200000",
            "climate": "arid",
            "terrain": "desert",
            "surface_water": "1",
            "swapi_url": "https://swapi.dev/api/planets/1/",
            "url": "http://localhost:8000/api/planets/1/",
            "created": timezone.now(),
            "edited": timezone.now(),
        }
        data.update(kwargs)
        return data

    def create_planet(self, **kwargs):
        return Planet.objects.create(**self.planet_data(**kwargs))

    def film_data(self, **kwargs):
        data = {
            "title": "A New Hope",
            "episode_id": 4,
            "opening_crawl": "It is a period of civil war...",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
            "swapi_url": "https://swapi.dev/api/films/1/",
            "url": "http://localhost:8000/api/films/1/",
            "created": timezone.now(),
            "edited": timezone.now(),
        }
        data.update(kwargs)
        return data

    def create_film(self, **kwargs):
        return Film.objects.create(**self.film_data(**kwargs))

    def species_data(self, homeworld=None, **kwargs):
        data = {
            "name": "Human",
            "classification": "mammal",
            "designation": "sentient",
            "average_height": "180",
            "average_lifespan": "120",
            "eye_colors": "brown, blue, green, hazel, grey, amber",
            "hair_colors": "blonde, brown, black, red",
            "skin_colors": "caucasian, black, asian, hispanic",
            "language": "Galactic Basic",
            "homeworld": homeworld,
            "swapi_url": "https://swapi.dev/api/species/1/",
            "url": "http://localhost:8000/api/species/1/",
            "created": timezone.now(),
            "edited": timezone.now(),
        }
        data.update(kwargs)
        return data

    def create_species(self, homeworld=None, **kwargs):
        return Species.objects.create(**self.species_data(homeworld=homeworld, **kwargs))

    def starship_data(self, **kwargs):
        data = {
            "name": "X-wing",
            "model": "T-65 X-wing",
            "starship_class": "Starfighter",
            "manufacturer": "Incom Corporation",
            "cost_in_credits": "149999",
            "length": "12.5",
            "crew": "1",
            "passengers": "0",
            "max_atmosphering_speed": "1050",
            "hyperdrive_rating": "1.0",
            "MGLT": "100",
            "cargo_capacity": "110",
            "consumables": "1 week",
            "swapi_url": "https://swapi.dev/api/starships/12/",
            "url": "http://localhost:8000/api/starships/12/",
            "created": timezone.now(),
            "edited": timezone.now(),
        }
        data.update(kwargs)
        return data

    def create_starship(self, **kwargs):
        return Starship.objects.create(**self.starship_data(**kwargs))

    def vehicle_data(self, **kwargs):
        data = {
            "name": "Snowspeeder",
            "model": "t-47 airspeeder",
            "vehicle_class": "airspeeder",
            "manufacturer": "Incom corporation",
            "length": "4.5",
            "cost_in_credits": "unknown",
            "crew": "2",
            "passengers": "0",
            "max_atmosphering_speed": "650",
            "cargo_capacity": "10",
            "consumables": "none",
            "swapi_url": "https://swapi.dev/api/vehicles/14/",
            "url": "http://localhost:8000/api/vehicles/14/",
            "created": timezone.now(),
            "edited": timezone.now(),
        }
        data.update(kwargs)
        return data

    def create_vehicle(self, **kwargs):
        return Vehicle.objects.create(**self.vehicle_data(**kwargs))

    def character_data(self, homeworld=None, **kwargs):
        data = {
            "name": "Luke Skywalker",
            "birth_year": "19BBY",
            "eye_color": "blue",
            "gender": "male",
            "hair_color": "blond",
            "height": "172",
            "mass": "77",
            "skin_color": "fair",
            "homeworld": homeworld,
            "swapi_url": "https://swapi.dev/api/people/1/",
            "url": "http://localhost:8000/api/people/1/",
            "created": timezone.now(),
            "edited": timezone.now(),
        }
        data.update(kwargs)
        return data

    def create_character(self, homeworld=None, **kwargs):
        return Character.objects.create(**self.character_data(homeworld=homeworld, **kwargs))