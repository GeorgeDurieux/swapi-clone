from django.test import TestCase

from core.serializers import (
    PlanetSerializer,
    FilmSerializer,
    SpeciesSerializer,
    StarshipSerializer,
    VehicleSerializer,
    CharacterSerializer,
)
from core.tests.helpers import DataHelperMixin


class TestPlanetSerializer(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet_payload = self.planet_data()

    def test_valid_serializer(self):
        serializer = PlanetSerializer(data=self.planet_payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_serializer_missing_field(self):
        data = self.planet_data()
        data.pop("name")

        serializer = PlanetSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_serializer_output(self):
        planet = self.create_planet()

        serializer = PlanetSerializer(planet)

        self.assertEqual(serializer.data["name"], "Tatooine")
        self.assertEqual(serializer.data["population"], "200000")
        self.assertEqual(serializer.data["climate"], "arid")
        self.assertEqual(serializer.data["rotation_period"], "23")
        self.assertEqual(serializer.data["gravity"], "1 standard")
        self.assertEqual(serializer.data["surface_water"], "1")
        self.assertEqual(serializer.data["swapi_url"], "https://swapi.dev/api/planets/1/")
        self.assertEqual(serializer.data["url"], "http://localhost:8000/api/planets/1/")


class TestFilmSerializer(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film_payload = self.film_data(planets=[self.planet.url])

    def test_valid_serializer(self):
        serializer = FilmSerializer(data=self.film_payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_serializer_missing_field(self):
        data = self.film_data(planets=[self.planet.url])
        data.pop("title")

        serializer = FilmSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_serializer_output(self):
        film = self.create_film()
        film.planets.add(self.planet)

        serializer = FilmSerializer(film)

        self.assertEqual(serializer.data["title"], "A New Hope")
        self.assertEqual(serializer.data["episode_id"], 4)
        self.assertEqual(serializer.data["planets"], [self.planet.url])


class TestSpeciesSerializer(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()
        self.species_payload = self.species_data(
            homeworld=self.planet.url,
            films=[self.film.url],
        )

    def test_valid_serializer(self):
        serializer = SpeciesSerializer(data=self.species_payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_serializer_missing_field(self):
        data = self.species_data(
            homeworld=self.planet.url,
            films=[self.film.url],
        )
        data.pop("name")

        serializer = SpeciesSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_serializer_output(self):
        species = self.create_species(homeworld=self.planet)
        species.films.add(self.film)

        serializer = SpeciesSerializer(species)

        self.assertEqual(serializer.data["name"], "Human")
        self.assertEqual(serializer.data["classification"], "mammal")
        self.assertEqual(serializer.data["designation"], "sentient")
        self.assertEqual(serializer.data["language"], "Galactic Basic")
        self.assertEqual(serializer.data["homeworld"], self.planet.url)
        self.assertEqual(serializer.data["films"], [self.film.url])


class TestStarshipSerializer(TestCase, DataHelperMixin):

    def setUp(self):
        self.film = self.create_film()
        self.starship_payload = self.starship_data(films=[self.film.url])

    def test_valid_serializer(self):
        serializer = StarshipSerializer(data=self.starship_payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_serializer_missing_field(self):
        data = self.starship_data(films=[self.film.url])
        data.pop("name")

        serializer = StarshipSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_serializer_output(self):
        starship = self.create_starship()
        starship.films.add(self.film)

        serializer = StarshipSerializer(starship)

        self.assertEqual(serializer.data["name"], "X-wing")
        self.assertEqual(serializer.data["model"], "T-65 X-wing")
        self.assertEqual(serializer.data["starship_class"], "Starfighter")
        self.assertEqual(serializer.data["films"], [self.film.url])


class TestVehicleSerializer(TestCase, DataHelperMixin):

    def setUp(self):
        self.film = self.create_film()
        self.vehicle_payload = self.vehicle_data(films=[self.film.url])

    def test_valid_serializer(self):
        serializer = VehicleSerializer(data=self.vehicle_payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_serializer_missing_field(self):
        data = self.vehicle_data(films=[self.film.url])
        data.pop("name")

        serializer = VehicleSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_serializer_output(self):
        vehicle = self.create_vehicle()
        vehicle.films.add(self.film)

        serializer = VehicleSerializer(vehicle)

        self.assertEqual(serializer.data["name"], "Snowspeeder")
        self.assertEqual(serializer.data["model"], "t-47 airspeeder")
        self.assertEqual(serializer.data["vehicle_class"], "airspeeder")
        self.assertEqual(serializer.data["films"], [self.film.url])


class TestCharacterSerializer(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()
        self.species = self.create_species(homeworld=self.planet)
        self.starship = self.create_starship()
        self.vehicle = self.create_vehicle()

        self.character_payload = self.character_data(
            homeworld=self.planet.url,
            films=[self.film.url],
            species=[self.species.url],
            starships=[self.starship.url],
            vehicles=[self.vehicle.url],
        )

    def test_valid_serializer(self):
        serializer = CharacterSerializer(data=self.character_payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_serializer_missing_field(self):
        data = self.character_data(
            homeworld=self.planet.url,
            films=[self.film.url],
            species=[self.species.url],
            starships=[self.starship.url],
            vehicles=[self.vehicle.url],
        )
        data.pop("name")

        serializer = CharacterSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_serializer_output(self):
        character = self.create_character(homeworld=self.planet)
        character.films.add(self.film)
        character.species.add(self.species)
        character.starships.add(self.starship)
        character.vehicles.add(self.vehicle)

        serializer = CharacterSerializer(character)

        self.assertEqual(serializer.data["name"], "Luke Skywalker")
        self.assertEqual(serializer.data["birth_year"], "19BBY")
        self.assertEqual(serializer.data["eye_color"], "blue")
        self.assertEqual(serializer.data["gender"], "male")
        self.assertEqual(serializer.data["homeworld"], self.planet.url)
        self.assertEqual(serializer.data["films"], [self.film.url])
        self.assertEqual(serializer.data["species"], [self.species.url])
        self.assertEqual(serializer.data["starships"], [self.starship.url])
        self.assertEqual(serializer.data["vehicles"], [self.vehicle.url])