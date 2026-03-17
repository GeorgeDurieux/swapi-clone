from rest_framework.routers import DefaultRouter

from .views import PlanetViewSet, FilmViewSet, SpeciesViewSet, StarshipViewSet, VehicleViewSet, CharacterViewSet

router = DefaultRouter()

router.register(r'planets', PlanetViewSet, basename='planets')
router.register(r'films', FilmViewSet, basename='films')
router.register(r'species', SpeciesViewSet, basename='species')
router.register(r'starships', StarshipViewSet, basename='starships')
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
router.register(r'characters', CharacterViewSet, basename='characters')

urlpatterns = router.urls