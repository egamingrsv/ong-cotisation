from django.shortcuts import render
from .models import Membre, Cotisation
from datetime import datetime
from django.http import HttpResponse
from reportlab.pdfgen import canvas

def home(request):
    return render(request, "home.html")

def verifier_cotisation(request):
    info = None

    if request.method == "POST":
        id_membre = request.POST.get("id_membre")

        try:
            membre = Membre.objects.get(id_membre=id_membre)
            cotisations = Cotisation.objects.filter(membre=membre)
            total = sum(c.montant for c in cotisations)

            # Calcul mois écoulés
            today = datetime.today()
            mois_ecoules = (today.year - membre.date_adhesion.year) * 12 + today.month - membre.date_adhesion.month

            montant_du = mois_ecoules * 10
            solde = total - montant_du

            statut = "À JOUR" if solde >= 0 else "EN RETARD"

            info = {
                "membre": membre,
                "cotisations": cotisations,
                "total": total,
                "statut": statut,
                "solde": solde
            }

        except Membre.DoesNotExist:
            info = "ID incorrect"

    return render(request, "verifier.html", {"info": info})

def generer_recu(request, cotisation_id):
    cotisation = Cotisation.objects.get(id=cotisation_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recu.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "REÇU DE COTISATION")
    p.drawString(100, 770, f"Membre: {cotisation.membre.nom}")
    p.drawString(100, 750, f"Mois: {cotisation.mois}")
    p.drawString(100, 730, f"Montant: {cotisation.montant} $")
    p.drawString(100, 710, f"Date: {cotisation.date_paiement}")

    p.showPage()
    p.save()

    return response