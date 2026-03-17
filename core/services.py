import os

import requests
from dotenv import load_dotenv

from .models import Planet, Film, Species, Starship, Vehicle, Character

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
SWAPI_URL = os.getenv("SWAPI_URL")

def fetch_data(endpoint):
    url = SWAPI_URL + endpoint
    data = []
    while url:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        results = response.json()
        data.extend(results.get("results", []))
        url = results.get("next")
    return data

def get_id(url):
    return url.rstrip('/').split("/")[-1]

def replace_swapi_urls(objects, category):
    updated = []

    for obj in objects:
        obj = obj.copy()
        obj["swapi_url"] = obj["url"]

        obj_id = get_id(obj["url"])
        obj['url'] = f'{BASE_URL}{category}/{obj_id}/'

        for key, value in obj.items():
            if key == "swapi_url":
                continue

            if isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, str) and item.startswith(SWAPI_URL):
                        obj_id = get_id(item)
                        endpoint = item[len(SWAPI_URL):].split('/')[0]
                        new_list.append(f'{BASE_URL}{endpoint}/{obj_id}/')
                    else:
                        new_list.append(item)
                obj[key] = new_list

            elif isinstance(value, str) and value.startswith(SWAPI_URL):
                obj_id = get_id(value)
                endpoint = value[len(SWAPI_URL):].split('/')[0]
                obj[key] = f'{BASE_URL}{endpoint}/{obj_id}/'

        updated.append(obj)
    return updated

def import_planets():
    planets = fetch_data("planets")
    planets = replace_swapi_urls(planets, "planets")

    for planet in planets:
        Planet.objects.update_or_create(
            swapi_url = planet["swapi_url"],
            defaults={
                "name": planet["name"],
                "diameter": planet["diameter"],
                "rotation_period": planet["rotation_period"],
                "orbital_period": planet["orbital_period"],
                "gravity": planet["gravity"],
                "population": planet["population"],
                "climate": planet["climate"],
                "terrain": planet["terrain"],
                "surface_water": planet["surface_water"],
                "url": planet["url"],
                "created": planet["created"],
                "edited": planet["edited"]
            }
        )

def import_films():
    films = fetch_data("films")
    films = replace_swapi_urls(films, "films")

    for film in films:
        film_obj, _ = Film.objects.update_or_create(
            swapi_url=film["swapi_url"],
            defaults={
                "title": film["title"],
                "episode_id": film["episode_id"],
                "opening_crawl": film["opening_crawl"],
                "director": film["director"],
                "producer": film["producer"],
                "release_date": film["release_date"],
                "url": film["url"],
                "created": film["created"],
                "edited": film["edited"]
            }
        )
        planet_urls = film.get("planets", [])
        planets = Planet.objects.filter(url__in=planet_urls)
        film_obj.planets.set(planets)

def import_species():
    species = fetch_data("species")
    species = replace_swapi_urls(species, "species")

    for spec in species:
        homeworld = None
        if spec.get("homeworld"):
            homeworld = Planet.objects.filter(url=spec["homeworld"]).first()

        species_obj, _ = Species.objects.update_or_create(
            swapi_url=spec["swapi_url"],
            defaults={
                "name": spec["name"],
                "classification": spec["classification"],
                "designation": spec["designation"],
                "average_height": spec["average_height"],
                "average_lifespan": spec["average_lifespan"],
                "eye_colors": spec["eye_colors"],
                "hair_colors": spec["hair_colors"],
                "skin_colors": spec["skin_colors"],
                "language": spec["language"],
                "homeworld": homeworld,
                "url": spec["url"],
                "created": spec["created"],
                "edited": spec["edited"]
            }
        )
        film_urls = spec.get("films", [])
        films = Film.objects.filter(url__in=film_urls)
        species_obj.films.set(films)

def import_starships():
    starships = fetch_data("starships")
    starships = replace_swapi_urls(starships, "starships")

    for starship in starships:
        starship_obj, _ = Starship.objects.update_or_create(
            swapi_url=starship["swapi_url"],
            defaults={
                "name": starship["name"],
                "model": starship["model"],
                "starship_class": starship["starship_class"],
                "manufacturer": starship["manufacturer"],
                "cost_in_credits": starship["cost_in_credits"],
                "length": starship["length"],
                "crew": starship["crew"],
                "passengers": starship["passengers"],
                "max_atmosphering_speed": starship["max_atmosphering_speed"],
                "hyperdrive_rating": starship["hyperdrive_rating"],
                "MGLT": starship["MGLT"],
                "cargo_capacity": starship["cargo_capacity"],
                "consumables": starship["consumables"],
                "url": starship["url"],
                "created": starship["created"],
                "edited": starship["edited"]
            }
        )
        film_urls = starship.get("films", [])
        films = Film.objects.filter(url__in=film_urls)
        starship_obj.films.set(films)

def import_vehicles():
    vehicles = fetch_data("vehicles")
    vehicles = replace_swapi_urls(vehicles, "vehicles")

    for vehicle in vehicles:
        vehicle_obj, _ = Vehicle.objects.update_or_create(
            swapi_url=vehicle["swapi_url"],
            defaults={
                "name": vehicle["name"],
                "model": vehicle["model"],
                "vehicle_class": vehicle["vehicle_class"],
                "manufacturer": vehicle["manufacturer"],
                "cost_in_credits": vehicle["cost_in_credits"],
                "length": vehicle["length"],
                "crew": vehicle["crew"],
                "passengers": vehicle["passengers"],
                "max_atmosphering_speed": vehicle["max_atmosphering_speed"],
                "cargo_capacity": vehicle["cargo_capacity"],
                "consumables": vehicle["consumables"],
                "url": vehicle["url"],
                "created": vehicle["created"],
                "edited": vehicle["edited"]
            }
        )
        film_urls = vehicle.get("films", [])
        films = Film.objects.filter(url__in=film_urls)
        vehicle_obj.films.set(films)

def import_characters():
    characters = fetch_data("people")
    characters = replace_swapi_urls(characters, "characters")

    for character in characters:
        homeworld = None
        if character.get("homeworld"):
            homeworld = Planet.objects.filter(url=character["homeworld"]).first()

        character_obj, _ = Character.objects.update_or_create(
            swapi_url=character["swapi_url"],
            defaults={
                "name": character["name"],
                "birth_year": character["birth_year"],
                "eye_color": character["eye_color"],
                "gender": character["gender"],
                "hair_color": character["hair_color"],
                "height": character["height"],
                "mass": character["mass"],
                "skin_color": character["skin_color"],
                "homeworld": homeworld,
                "url": character["url"],
                "created": character["created"],
                "edited": character["edited"]
            }
        )
        film_urls = character.get("films", [])
        films = Film.objects.filter(url__in=film_urls)
        character_obj.films.set(films)

        species_urls = character.get("species", [])
        species = Species.objects.filter(url__in=species_urls)
        character_obj.species.set(species)

        starship_urls = character.get("starships", [])
        starships = Starship.objects.filter(url__in=starship_urls)
        character_obj.starships.set(starships)

        vehicle_urls = character.get("vehicles", [])
        vehicles = Vehicle.objects.filter(url__in=vehicle_urls)
        character_obj.vehicles.set(vehicles)



