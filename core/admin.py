from django.contrib import admin

from .models import Film, Character, Vehicle, Planet, Species, Starship

admin.site.register(Planet)
admin.site.register(Film)
admin.site.register(Species)
admin.site.register(Starship)
admin.site.register(Vehicle)
admin.site.register(Character)
