from django.test import TestCase
from django.db import IntegrityError

from core.models import Planet, Film, Species, Starship, Vehicle, Character
from core.tests.helpers import DataHelperMixin


class TestPlanetModel(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet_data = self.planet_data()

    def test_create_planet(self):
        planet = Planet.objects.create(**self.planet_data)

        self.assertEqual(planet.name, "Tatooine")
        self.assertEqual(planet.population, "200000")
        self.assertEqual(Planet.objects.count(), 1)

    def test_planet_str(self):
        planet = Planet.objects.create(**self.planet_data)

        self.assertEqual(str(planet), "Tatooine")

    def test_swapi_url_unique(self):
        Planet.objects.create(**self.planet_data)

        with self.assertRaises(IntegrityError):
            Planet.objects.create(**self.planet_data)


class TestFilmModel(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film_data = self.film_data()

    def test_create_film(self):
        film = Film.objects.create(**self.film_data)

        self.assertEqual(film.title, "A New Hope")
        self.assertEqual(film.episode_id, 4)
        self.assertEqual(Film.objects.count(), 1)

    def test_film_str(self):
        film = Film.objects.create(**self.film_data)

        self.assertEqual(str(film), "A New Hope")

    def test_swapi_url_unique(self):
        Film.objects.create(**self.film_data)

        with self.assertRaises(IntegrityError):
            Film.objects.create(**self.film_data)

    def test_film_planets_relationship(self):
        film = Film.objects.create(**self.film_data)
        film.planets.add(self.planet)

        self.assertEqual(film.planets.count(), 1)
        self.assertIn(self.planet, film.planets.all())
        self.assertIn(film, self.planet.films.all())


class TestSpeciesModel(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()
        self.species_data = self.species_data(homeworld=self.planet)

    def test_create_species(self):
        species = Species.objects.create(**self.species_data)

        self.assertEqual(species.name, "Human")
        self.assertEqual(species.classification, "mammal")
        self.assertEqual(species.homeworld, self.planet)
        self.assertEqual(Species.objects.count(), 1)

    def test_species_str(self):
        species = Species.objects.create(**self.species_data)

        self.assertEqual(str(species), "Human")

    def test_swapi_url_unique(self):
        Species.objects.create(**self.species_data)

        with self.assertRaises(IntegrityError):
            Species.objects.create(**self.species_data)

    def test_species_films_relationship(self):
        species = Species.objects.create(**self.species_data)
        species.films.add(self.film)

        self.assertEqual(species.films.count(), 1)
        self.assertIn(self.film, species.films.all())
        self.assertIn(species, self.film.species.all())

    def test_species_homeworld_can_be_null(self):
        data = self.species_data.copy()
        data["homeworld"] = None

        species = Species.objects.create(**data)

        self.assertIsNone(species.homeworld)


class TestStarshipModel(TestCase, DataHelperMixin):

    def setUp(self):
        self.film = self.create_film()
        self.starship_data = self.starship_data()

    def test_create_starship(self):
        starship = Starship.objects.create(**self.starship_data)

        self.assertEqual(starship.name, "X-wing")
        self.assertEqual(starship.model, "T-65 X-wing")
        self.assertEqual(Starship.objects.count(), 1)

    def test_starship_str(self):
        starship = Starship.objects.create(**self.starship_data)

        self.assertEqual(str(starship), "X-wing")

    def test_swapi_url_unique(self):
        Starship.objects.create(**self.starship_data)

        with self.assertRaises(IntegrityError):
            Starship.objects.create(**self.starship_data)

    def test_starship_films_relationship(self):
        starship = Starship.objects.create(**self.starship_data)
        starship.films.add(self.film)

        self.assertEqual(starship.films.count(), 1)
        self.assertIn(self.film, starship.films.all())
        self.assertIn(starship, self.film.starships.all())


class TestVehicleModel(TestCase, DataHelperMixin):

    def setUp(self):
        self.film = self.create_film()
        self.vehicle_data = self.vehicle_data()

    def test_create_vehicle(self):
        vehicle = Vehicle.objects.create(**self.vehicle_data)

        self.assertEqual(vehicle.name, "Snowspeeder")
        self.assertEqual(vehicle.model, "t-47 airspeeder")
        self.assertEqual(vehicle.manufacturer, "Incom corporation")
        self.assertEqual(vehicle.length, "4.5")
        self.assertEqual(vehicle.cost_in_credits, "unknown")
        self.assertEqual(vehicle.crew, "2")
        self.assertEqual(vehicle.passengers, "0")
        self.assertEqual(vehicle.max_atmosphering_speed, "650")
        self.assertEqual(vehicle.cargo_capacity, "10")
        self.assertEqual(vehicle.consumables, "none")
        self.assertEqual(vehicle.swapi_url, "https://swapi.dev/api/vehicles/14/")
        self.assertEqual(vehicle.url, "http://localhost:8000/api/vehicles/14/")
        self.assertEqual(Vehicle.objects.count(), 1)

    def test_vehicle_str(self):
        vehicle = Vehicle.objects.create(**self.vehicle_data)

        self.assertEqual(str(vehicle), "Snowspeeder")

    def test_swapi_url_unique(self):
        Vehicle.objects.create(**self.vehicle_data)

        with self.assertRaises(IntegrityError):
            Vehicle.objects.create(**self.vehicle_data)

    def test_vehicle_films_relationship(self):
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        vehicle.films.add(self.film)

        self.assertEqual(vehicle.films.count(), 1)
        self.assertIn(self.film, vehicle.films.all())
        self.assertIn(vehicle, self.film.vehicles.all())


class TestCharacterModel(TestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()
        self.species = self.create_species(homeworld=self.planet)
        self.starship = self.create_starship()
        self.vehicle = self.create_vehicle()
        self.character_data = self.character_data(homeworld=self.planet)

    def test_create_character(self):
        character = Character.objects.create(**self.character_data)

        self.assertEqual(character.name, "Luke Skywalker")
        self.assertEqual(character.birth_year, "19BBY")
        self.assertEqual(character.eye_color, "blue")
        self.assertEqual(character.gender, "male")
        self.assertEqual(character.hair_color, "blond")
        self.assertEqual(character.height, "172")
        self.assertEqual(character.mass, "77")
        self.assertEqual(character.skin_color, "fair")
        self.assertEqual(character.homeworld, self.planet)
        self.assertEqual(character.swapi_url, "https://swapi.dev/api/people/1/")
        self.assertEqual(character.url, "http://localhost:8000/api/people/1/")
        self.assertEqual(Character.objects.count(), 1)

    def test_character_str(self):
        character = Character.objects.create(**self.character_data)

        self.assertEqual(str(character), "Luke Skywalker")

    def test_swapi_url_unique(self):
        Character.objects.create(**self.character_data)

        with self.assertRaises(IntegrityError):
            Character.objects.create(**self.character_data)

    def test_character_films_relationship(self):
        character = Character.objects.create(**self.character_data)
        character.films.add(self.film)

        self.assertEqual(character.films.count(), 1)
        self.assertIn(self.film, character.films.all())
        self.assertIn(character, self.film.characters.all())

    def test_character_species_relationship(self):
        character = Character.objects.create(**self.character_data)
        character.species.add(self.species)

        self.assertEqual(character.species.count(), 1)
        self.assertIn(self.species, character.species.all())
        self.assertIn(character, self.species.characters.all())

    def test_character_starships_relationship(self):
        character = Character.objects.create(**self.character_data)
        character.starships.add(self.starship)

        self.assertEqual(character.starships.count(), 1)
        self.assertIn(self.starship, character.starships.all())
        self.assertIn(character, self.starship.pilots.all())

    def test_character_vehicles_relationship(self):
        character = Character.objects.create(**self.character_data)
        character.vehicles.add(self.vehicle)

        self.assertEqual(character.vehicles.count(), 1)
        self.assertIn(self.vehicle, character.vehicles.all())
        self.assertIn(character, self.vehicle.pilots.all())