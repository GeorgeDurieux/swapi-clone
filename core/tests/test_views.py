from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from django.urls import reverse

from core.models import Planet, Film, Species, Starship, Vehicle, Character
from core.tests.helpers import DataHelperMixin


class TestPlanetAPI(APITestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()

    def test_get_all_planets(self):
        url = reverse("planets-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_planet(self):
        url = reverse("planets-detail", args=[self.planet.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Tatooine")

    def test_create_planet(self):
        url = reverse("planets-list")

        data = self.planet_data(
            name="Naboo",
            diameter="12120",
            rotation_period="26",
            orbital_period="312",
            population="4500000000",
            climate="temperate",
            terrain="grassy hills",
            surface_water="12",
            swapi_url="https://swapi.dev/api/planets/8/",
            url="http://localhost:8000/api/planets/8/",
            created=timezone.now(),
            edited=timezone.now(),
        )

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Planet.objects.count(), 2)
        self.assertEqual(response.data["name"], "Naboo")


class TestFilmAPI(APITestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()
        self.film.planets.add(self.planet)

    def test_get_all_films(self):
        url = reverse("films-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_film(self):
        url = reverse("films-detail", args=[self.film.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "A New Hope")

    def test_create_film(self):
        url = reverse("films-list")

        data = self.film_data(
            title="The Empire Strikes Back",
            episode_id=5,
            opening_crawl="It is a dark time for the Rebellion...",
            director="Irvin Kershner",
            release_date="1980-05-17",
            planets=[self.planet.url],
            swapi_url="https://swapi.dev/api/films/2/",
            url="http://localhost:8000/api/films/2/",
            created=timezone.now(),
            edited=timezone.now(),
        )

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 2)
        self.assertEqual(response.data["title"], "The Empire Strikes Back")
        self.assertEqual(response.data["planets"], [self.planet.url])


class TestSpeciesAPI(APITestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()
        self.species = self.create_species(homeworld=self.planet)
        self.species.films.add(self.film)

    def test_get_all_species(self):
        url = reverse("species-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_species(self):
        url = reverse("species-detail", args=[self.species.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Human")

    def test_create_species(self):
        url = reverse("species-list")

        data = self.species_data(
            name="Droid",
            classification="artificial",
            average_height="n/a",
            average_lifespan="indefinite",
            eye_colors="red, blue, yellow",
            hair_colors="none",
            skin_colors="white, blue, red, silver",
            language="n/a",
            homeworld=self.planet.url,
            films=[self.film.url],
            swapi_url="https://swapi.dev/api/species/2/",
            url="http://localhost:8000/api/species/2/",
            created=timezone.now(),
            edited=timezone.now(),
        )

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Species.objects.count(), 2)
        self.assertEqual(response.data["name"], "Droid")
        self.assertEqual(response.data["homeworld"], self.planet.url)
        self.assertEqual(response.data["films"], [self.film.url])


class TestStarshipAPI(APITestCase, DataHelperMixin):

    def setUp(self):
        self.film = self.create_film()
        self.starship = self.create_starship()
        self.starship.films.add(self.film)

    def test_get_all_starships(self):
        url = reverse("starships-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_starship(self):
        url = reverse("starships-detail", args=[self.starship.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "X-wing")

    def test_create_starship(self):
        url = reverse("starships-list")

        data = self.starship_data(
            name="Death Star",
            model="DS-1 Orbital Battle Station",
            starship_class="Deep Space Mobile Battlestation",
            manufacturer="Imperial Department of Military Research, Sienar Fleet Systems",
            cost_in_credits="1000000000000",
            length="120000",
            crew="342953",
            passengers="843342",
            max_atmosphering_speed="n/a",
            hyperdrive_rating="4.0",
            MGLT="10",
            cargo_capacity="1000000000000",
            consumables="3 years",
            films=[self.film.url],
            swapi_url="https://swapi.dev/api/starships/9/",
            url="http://localhost:8000/api/starships/9/",
            created=timezone.now(),
            edited=timezone.now(),
        )

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Starship.objects.count(), 2)
        self.assertEqual(response.data["name"], "Death Star")
        self.assertEqual(response.data["films"], [self.film.url])


class TestVehicleAPI(APITestCase, DataHelperMixin):

    def setUp(self):
        self.film = self.create_film()
        self.vehicle = self.create_vehicle()
        self.vehicle.films.add(self.film)

    def test_get_all_vehicles(self):
        url = reverse("vehicles-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_vehicle(self):
        url = reverse("vehicles-detail", args=[self.vehicle.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Snowspeeder")

    def test_create_vehicle(self):
        url = reverse("vehicles-list")

        data = self.vehicle_data(
            name="Sand Crawler",
            model="Digger Crawler",
            vehicle_class="wheeled",
            manufacturer="Corellia Mining Corporation",
            length="36.8",
            cost_in_credits="150000",
            crew="46",
            passengers="30",
            max_atmosphering_speed="30",
            cargo_capacity="50000",
            consumables="2 months",
            films=[self.film.url],
            swapi_url="https://swapi.dev/api/vehicles/4/",
            url="http://localhost:8000/api/vehicles/4/",
            created=timezone.now(),
            edited=timezone.now(),
        )

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 2)
        self.assertEqual(response.data["name"], "Sand Crawler")
        self.assertEqual(response.data["films"], [self.film.url])


class TestCharacterAPI(APITestCase, DataHelperMixin):

    def setUp(self):
        self.planet = self.create_planet()
        self.film = self.create_film()
        self.species = self.create_species(homeworld=self.planet)
        self.starship = self.create_starship()
        self.vehicle = self.create_vehicle()
        self.character = self.create_character(homeworld=self.planet)

        self.character.films.add(self.film)
        self.character.species.add(self.species)
        self.character.starships.add(self.starship)
        self.character.vehicles.add(self.vehicle)

    def test_get_all_characters(self):
        url = reverse("characters-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_character(self):
        url = reverse("characters-detail", args=[self.character.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Luke Skywalker")

    def test_create_character(self):
        url = reverse("characters-list")

        data = self.character_data(
            name="Leia Organa",
            eye_color="brown",
            gender="female",
            hair_color="brown",
            height="150",
            mass="49",
            skin_color="light",
            homeworld=self.planet.url,
            films=[self.film.url],
            species=[self.species.url],
            starships=[self.starship.url],
            vehicles=[self.vehicle.url],
            swapi_url="https://swapi.dev/api/people/5/",
            url="http://localhost:8000/api/people/5/",
            created=timezone.now(),
            edited=timezone.now(),
        )

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Character.objects.count(), 2)
        self.assertEqual(response.data["name"], "Leia Organa")
        self.assertEqual(response.data["homeworld"], self.planet.url)
        self.assertEqual(response.data["films"], [self.film.url])
        self.assertEqual(response.data["species"], [self.species.url])
        self.assertEqual(response.data["starships"], [self.starship.url])
        self.assertEqual(response.data["vehicles"], [self.vehicle.url])