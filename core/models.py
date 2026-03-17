from django.db import models


class Planet(models.Model):
    name = models.CharField(max_length=255)
    diameter = models.CharField(max_length=50)
    rotation_period = models.CharField(max_length=50)
    orbital_period = models.CharField(max_length=50)
    gravity = models.CharField(max_length=50)
    population = models.CharField(max_length=100)
    climate = models.CharField(max_length=255)
    terrain = models.CharField(max_length=255)
    surface_water = models.CharField(max_length=50)
    swapi_url = models.URLField(unique=True)
    url = models.URLField(unique=True)
    created = models.DateTimeField()
    edited = models.DateTimeField()

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=255)
    episode_id = models.IntegerField()
    opening_crawl = models.TextField()
    director = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    release_date = models.DateField()
    swapi_url = models.URLField(unique=True)
    url = models.URLField(unique=True)
    created = models.DateTimeField()
    edited = models.DateTimeField()
    planets = models.ManyToManyField(Planet, related_name='films', blank=True)

    def __str__(self):
        return self.title


class Species(models.Model):
    name = models.CharField(max_length=255)
    classification = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    average_height = models.CharField(max_length=50)
    average_lifespan = models.CharField(max_length=50)
    eye_colors = models.CharField(max_length=255)
    hair_colors = models.CharField(max_length=255)
    skin_colors = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    homeworld = models.ForeignKey(
        Planet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='species_set'
    )
    swapi_url = models.URLField(unique=True)
    url = models.URLField(unique=True)
    created = models.DateTimeField()
    edited = models.DateTimeField()
    films = models.ManyToManyField(Film, related_name='species', blank=True)

    def __str__(self):
        return self.name


class Starship(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    starship_class = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    cost_in_credits = models.CharField(max_length=100)
    length = models.CharField(max_length=100)
    crew = models.CharField(max_length=100)
    passengers = models.CharField(max_length=100)
    max_atmosphering_speed = models.CharField(max_length=100)
    hyperdrive_rating = models.CharField(max_length=100)
    MGLT = models.CharField(max_length=100)
    cargo_capacity = models.CharField(max_length=100)
    consumables = models.CharField(max_length=100)
    swapi_url = models.URLField(unique=True)
    url = models.URLField(unique=True)
    created = models.DateTimeField()
    edited = models.DateTimeField()
    films = models.ManyToManyField(Film, related_name='starships', blank=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    vehicle_class = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    length = models.CharField(max_length=100)
    cost_in_credits = models.CharField(max_length=100)
    crew = models.CharField(max_length=100)
    passengers = models.CharField(max_length=100)
    max_atmosphering_speed = models.CharField(max_length=100)
    cargo_capacity = models.CharField(max_length=100)
    consumables = models.CharField(max_length=100)
    swapi_url = models.URLField(unique=True)
    url = models.URLField(unique=True)
    created = models.DateTimeField()
    edited = models.DateTimeField()
    films = models.ManyToManyField(Film, related_name='vehicles', blank=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255)
    birth_year = models.CharField(max_length=50)
    eye_color = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=100)
    height = models.CharField(max_length=50)
    mass = models.CharField(max_length=50)
    skin_color = models.CharField(max_length=100)
    homeworld = models.ForeignKey(
        Planet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='residents'
    )
    swapi_url = models.URLField(unique=True)
    url = models.URLField(unique=True)
    created = models.DateTimeField()
    edited = models.DateTimeField()
    films = models.ManyToManyField(Film, related_name='characters', blank=True)
    species = models.ManyToManyField(Species, related_name='characters', blank=True)
    starships = models.ManyToManyField(Starship, related_name='pilots', blank=True)
    vehicles = models.ManyToManyField(Vehicle, related_name='pilots', blank=True)

    def __str__(self):
        return self.name