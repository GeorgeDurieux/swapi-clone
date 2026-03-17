from unittest.mock import patch

from django.test import TestCase

from core import services
from core.models import Planet, Film, Species, Starship, Vehicle, Character
from core.tests.helpers import DataHelperMixin


class TestUtilityFunctions(TestCase):

    def test_get_id(self):
        self.assertEqual(services.get_id("https://swapi.dev/api/planets/1/"), "1")
        self.assertEqual(services.get_id("http://localhost:8000/api/films/4/"), "4")

    @patch("core.services.SWAPI_URL", "https://swapi.dev/api/")
    @patch("core.services.BASE_URL", "http://localhost:8000/api/")
    def test_replace_swapi_urls(self):
        objects = [
            {
                "name": "Tatooine",
                "url": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                ],
                "residents": [
                    "https://swapi.dev/api/people/1/",
                ],
            }
        ]

        result = services.replace_swapi_urls(objects, "planets")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["swapi_url"], "https://swapi.dev/api/planets/1/")
        self.assertEqual(result[0]["url"], "http://localhost:8000/api/planets/1/")
        self.assertEqual(
            result[0]["films"],
            [
                "http://localhost:8000/api/films/1/",
                "http://localhost:8000/api/films/2/",
            ],
        )
        self.assertEqual(
            result[0]["residents"],
            ["http://localhost:8000/api/people/1/"],
        )


class TestImportPlanets(TestCase, DataHelperMixin):

    @patch("core.services.fetch_data")
    @patch("core.services.replace_swapi_urls")
    def test_import_planets(self, mock_replace_swapi_urls, mock_fetch_data):
        mock_fetch_data.return_value = [{}]
        mock_replace_swapi_urls.return_value = [self.planet_data()]

        services.import_planets()
        self.assertEqual(Planet.objects.count(), 1)

        planet = Planet.objects.get()
        self.assertEqual(planet.name, "Tatooine")
        self.assertEqual(planet.swapi_url, "https://swapi.dev/api/planets/1/")
        self.assertEqual(planet.url, "http://localhost:8000/api/planets/1/")

class TestImportFilms(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()

    @patch("core.services.fetch_data")
    @patch("core.services.replace_swapi_urls")
    def test_import_films(self, mock_replace_swapi_urls, mock_fetch_data):
        mock_fetch_data.return_value = [{}]
        mock_replace_swapi_urls.return_value = [
            {
                "title": "A New Hope",
                "episode_id": 4,
                "opening_crawl": "It is a period of civil war.\r\nRebel spaceships, striking\r\nfrom a hidden base, have won\r\ntheir first victory against\r\nthe evil Galactic Empire.\r\n\r\nDuring the battle, Rebel\r\nspies managed to steal secret\r\nplans to the Empire's\r\nultimate weapon, the DEATH\r\nSTAR, an armored space\r\nstation with enough power\r\nto destroy an entire planet.\r\n\r\nPursued by the Empire's\r\nsinister agents, Princess\r\nLeia races home aboard her\r\nstarship, custodian of the\r\nstolen plans that can save her\r\npeople and restore\r\nfreedom to the galaxy....",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25",
                "planets": [self.planet.url],
                "created": "2014-12-10T14:23:31.880000Z",
                "edited": "2014-12-20T19:49:45.256000Z",
                "url": "https://localhost:8000/api/films/1/",
                "swapi_url": "https://swapi.dev/api/films/1/"
            }
        ]

        services.import_films()
        self.assertEqual(Film.objects.count(), 1)

        film = Film.objects.get()
        self.assertEqual(film.title, "A New Hope")
        self.assertEqual(film.episode_id, 4)
        self.assertIn(self.planet, film.planets.all())

class TestImportSpecies(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()

    @patch("core.services.fetch_data")
    @patch("core.services.replace_swapi_urls")
    def test_import_species(self, mock_replace_swapi_urls, mock_fetch_data):
        mock_fetch_data.return_value = [{}]
        mock_replace_swapi_urls.return_value = [
            {
                "name": "Human",
                "classification": "mammal",
                "designation": "sentient",
                "average_height": "180",
                "average_lifespan": "120",
                "eye_colors": "brown, blue, green, hazel, grey, amber",
                "hair_colors": "blonde, brown, black, red",
                "skin_colors": "caucasian, black, asian, hispanic",
                "language": "Galactic Basic",
                "homeworld": self.planet.url,
                "films": [self.film.url],
                "created": "2014-12-10T13:52:11.567000Z",
                "edited": "2014-12-20T21:36:42.136000Z",
                "url": "http://localhost:8000/api/species/1/",
                "swapi_url": "https://swapi.dev/api/species/1/"
            }
        ]

        services.import_species()
        self.assertEqual(Species.objects.count(), 1)

        species = Species.objects.get()
        self.assertEqual(species.name, "Human")
        self.assertEqual(species.classification, "mammal")
        self.assertEqual(species.homeworld, self.planet)
        self.assertIn(self.film, species.films.all())

    @patch("core.services.fetch_data")
    @patch("core.services.replace_swapi_urls")
    def test_import_species_no_homeworld(self, mock_replace_swapi_urls, mock_fetch_data):
        mock_fetch_data.return_value = [{}]
        mock_replace_swapi_urls.return_value = [
            {
                "name": "Human",
                "classification": "mammal",
                "designation": "sentient",
                "average_height": "180",
                "average_lifespan": "120",
                "eye_colors": "brown, blue, green, hazel, grey, amber",
                "hair_colors": "blonde, brown, black, red",
                "skin_colors": "caucasian, black, asian, hispanic",
                "language": "Galactic Basic",
                "homeworld": None,
                "films": [],
                "created": "2014-12-10T13:52:11.567000Z",
                "edited": "2014-12-20T21:36:42.136000Z",
                "url": "http://localhost:8000/api/species/1/",
                "swapi_url": "https://swapi.dev/api/species/1/"
            }
        ]

        services.import_species()
        self.assertEqual(Species.objects.count(), 1)

        species = Species.objects.get()
        self.assertEqual(species.name, "Human")
        self.assertEqual(species.classification, "mammal")
        self.assertEqual(species.homeworld, None)
        self.assertEqual(species.films.count(), 0)

class TestImportStarships(TestCase, DataHelperMixin):

    def setUp(self):
        self.film = self.create_film()

    @patch("core.services.fetch_data")
    @patch("core.services.replace_swapi_urls")
    def test_import_starships(self, mock_replace_swapi_urls, mock_fetch_data):
        mock_fetch_data.return_value = [{}]
        mock_replace_swapi_urls.return_value = [
            {
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
                "pilots": [],
                "films": [self.film.url],
                "created": "2014-12-12T11:19:05.340000Z",
                "edited": "2014-12-20T21:23:49.886000Z",
                "url": "http://localhost:8000/api/starships/12/",
                "swapi_url": "https://swapi.dev/api/starships/12/",
            }
        ]

        services.import_starships()
        self.assertEqual(Starship.objects.count(), 1)

        starship = Starship.objects.get()
        self.assertEqual(starship.name, "X-wing")
        self.assertEqual(starship.manufacturer, "Incom Corporation")
        self.assertIn(self.film, starship.films.all())

class TestImportVehicles(TestCase, DataHelperMixin):

    def setUp(self):
        self.film = self.create_film()

    @patch("core.services.fetch_data")
    @patch("core.services.replace_swapi_urls")
    def test_import_vehicles(self, mock_replace_swapi_urls, mock_fetch_data):
        mock_fetch_data.return_value = [{}]
        mock_replace_swapi_urls.return_value = [
            {
                "name": "Sand Crawler",
                "model": "Digger Crawler",
                "manufacturer": "Corellia Mining Corporation",
                "cost_in_credits": "150000",
                "length": "36.8 ",
                "max_atmosphering_speed": "30",
                "crew": "46",
                "passengers": "30",
                "cargo_capacity": "50000",
                "consumables": "2 months",
                "vehicle_class": "wheeled",
                "pilots": [],
                "films": [self.film.url],
                "created": "2014-12-10T15:36:25.724000Z",
                "edited": "2014-12-20T21:30:21.661000Z",
                "url": "https://localhost:8000/api/vehicles/4/",
                "swapi_url": "https://swapi.dev/api/vehicles/4/"
            }
        ]

        services.import_vehicles()
        self.assertEqual(Vehicle.objects.count(), 1)

        vehicle = Vehicle.objects.get()
        self.assertEqual(vehicle.name, "Sand Crawler")
        self.assertEqual(vehicle.manufacturer, "Corellia Mining Corporation")
        self.assertIn(self.film, vehicle.films.all())

class TeestImportCharacters(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()
        self.species = self.create_species()
        self.starship = self.create_starship()
        self.vehicle = self.create_vehicle()

    @patch("core.services.fetch_data")
    @patch("core.services.replace_swapi_urls")
    def test_import_characters(self, mock_replace_swapi_urls, mock_fetch_data):
        mock_fetch_data.return_value = [{}]
        mock_replace_swapi_urls.return_value = [
            {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": self.planet.url,
                "films": [self.film.url],
                "species": [self.species.url],
                "vehicles": [self.vehicle.url],
                "starships": [self.starship.url],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.dev/api/people/1/"
            },
        ]

        services.import_characters()
        self.assertEqual(Character.objects.count(), 1)

        character = Character.objects.get()
        self.assertEqual(character.name, "Luke Skywalker")
        self.assertEqual(character.homeworld, self.planet.url)
        self.assertIn(self.film, character.films.all())
        self.assertIn(self.species, character.species.all())
        self.assertIn(self.starship, character.starships.all())
        self.assertIn(self.vehicle, character.vehicles.all())
