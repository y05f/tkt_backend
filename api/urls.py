from django.urls import path, re_path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path(
        "entreprise/",
        views.EntrepriseListCreate.as_view(),
        name="list-create-entreprise",
    ),
    re_path(
        r"^entreprise/(?P<siren>[0-9]{9})/$",
        views.EntrepriseRetrieveUpdateDestroy.as_view(),
        name="entreprise-details",
    ),
    path(
        "entreprise/name/",
        views.EntrepriseNamesOnly.as_view(),
        name="list-entreprise-name",
    ),
    path(
        "entreprise/name/<str:name>",
        views.EntrepriseNameDetails.as_view(),
        name="entreprise-name-details",
    ),
    path(
        "entreprise/stats/<str:name>",
        views.EntrepriseNameStats.as_view(),
        name="entreprise-name-stats",
    ),
    # Optional UI:
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("shema", SpectacularAPIView.as_view(), name="schema"),
]
