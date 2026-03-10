from django.db import models

class Membre(models.Model):
    id_membre = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    date_adhesion = models.DateField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} ({self.id_membre})"


class Cotisation(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    mois = models.CharField(max_length=20)  # ex: Janvier 2026
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.membre.nom} - {self.mois}"