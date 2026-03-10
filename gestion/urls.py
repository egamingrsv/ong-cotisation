from django.urls import path
from .views import verifier_cotisation, generer_recu

urlpatterns = [
    path("verifier/", verifier_cotisation, name="verifier"),
    path("recu/<int:cotisation_id>/", generer_recu, name="recu"),
]