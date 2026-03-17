from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Planet, Film, Species, Starship, Vehicle, Character


class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = "__all__"

    def validate_population(self, value):
        if not value.isdigit() and value.lower() != "unknown":
            raise ValidationError("Population must be a number or unknown")
        return value

    def validate_diameter(self, value):
        if not value.isdigit() and value.lower() != "unknown":
            raise ValidationError("Diameter must be a number or unknown")
        return value

    def validate_rotation_period(self, value):
        if not value.isdigit() and value.lower() != "unknown":
            raise ValidationError("Rotation period must be a number or unknown")
        return value

    def validate_orbital_period(self, value):
        if not value.isdigit() and value.lower() != "unknown":
            raise ValidationError("Orbital period must be a number or unknown")
        return value

    def validate_surface_water(self, value):
        if not value.isdigit() and value.lower() != "unknown":
            raise ValidationError("Surface water must be a number or unknown")
        return value


class FilmSerializer(serializers.ModelSerializer):
    planets = serializers.SlugRelatedField(
        many=True,
        slug_field="url",
        queryset=Planet.objects.all(),
        required=False
    )

    class Meta:
        model = Film
        fields = "__all__"

    def validate_director(self, value):
        if value in ["J. J. Abrams", "Rian Johnson"]:
            raise ValidationError("This is shit, not Star Wars")
        return value


class SpeciesSerializer(serializers.ModelSerializer):
    homeworld = serializers.SlugRelatedField(
        slug_field="url",
        queryset=Planet.objects.all(),
        allow_null=True,
        required=False
    )
    films = serializers.SlugRelatedField(
        many=True,
        slug_field="url",
        queryset=Film.objects.all(),
        required=False
    )

    class Meta:
        model = Species
        fields = "__all__"


class StarshipSerializer(serializers.ModelSerializer):
    films = serializers.SlugRelatedField(
        many=True,
        slug_field="url",
        queryset=Film.objects.all(),
        required=False
    )

    class Meta:
        model = Starship
        fields = "__all__"

    def validate_cost_in_credits(self, value):
        if not value.isdigit() and value.lower() != "unknown":
            raise ValidationError("Cost must be a number or unknown")
        return value


class VehicleSerializer(serializers.ModelSerializer):
    films = serializers.SlugRelatedField(
        many=True,
        slug_field="url",
        queryset=Film.objects.all(),
        required=False
    )

    class Meta:
        model = Vehicle
        fields = "__all__"

    def validate_cost_in_credits(self, value):
        if not value.isdigit() and value.lower() not in ["unknown", "n/a"]:
            raise ValidationError("Cost must be a number, unknown, or n/a")
        return value


class CharacterSerializer(serializers.ModelSerializer):
    homeworld = serializers.SlugRelatedField(
        slug_field="url",
        queryset=Planet.objects.all(),
        allow_null=True,
        required=False
    )
    films = serializers.SlugRelatedField(
        many=True,
        slug_field="url",
        queryset=Film.objects.all(),
        required=False
    )
    species = serializers.SlugRelatedField(
        many=True,
        slug_field="url",
        queryset=Species.objects.all(),
        required=False
    )
    starships = serializers.SlugRelatedField(
        many=True,
        slug_field="url",
        queryset=Starship.objects.all(),
        required=False
    )
    vehicles = serializers.SlugRelatedField(
        many=True,
        slug_field="url",
        queryset=Vehicle.objects.all(),
        required=False
    )

    class Meta:
        model = Character
        fields = "__all__"