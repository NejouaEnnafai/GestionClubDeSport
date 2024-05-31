from django.contrib import admin
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from .views import *
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import Membre, Adhesion, Activite, MembreActivite, Evenement, MembreEvenement, Ressource, Reservation



@admin.register(Adhesion)
class AdhesionAdmin(admin.ModelAdmin):
    list_display = ('membre', 'date_debut', 'date_fin', 'montant_paye')
    list_filter = ('date_debut', 'date_fin')

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date', 'heure', 'lieu' )

@admin.register(MembreActivite)
class MembreActiviteAdmin(admin.ModelAdmin):
    list_display = ('membre', 'activite')

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date', 'heure', 'lieu','affiche')

@admin.register(MembreEvenement)
class MembreEvenementAdmin(admin.ModelAdmin):
    list_display = ('membre', 'evenement')

@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'disponibilite')
    list_filter = ('type', 'disponibilite')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('ressource', 'date', 'heure', 'membre')
    list_filter = ('date', 'heure')





from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import Membre

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    actions = ['telecharger_rapport']

    def telecharger_rapport(self, request, queryset):
        # Générez le contenu du PDF ici
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="rapport_membres.pdf"'

        # Créez un document PDF avec ReportLab
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
          # Ajoutez un titre en haut de la première page
        title_style = getSampleStyleSheet()['Title']
        title_text = "Liste des membres"
        title = Paragraph(title_text, title_style)
        elements.append(title)
        # Créez un tableau pour afficher les données des membres
        data = [[
            "Prénom",
            "Nom",
            "Email",
            "Adresse",
            "Contact",
            "Statut",
        ]]

        for membre in queryset:
            data.append([
                membre.prenom,
                membre.nom,
                membre.email,
                membre.adresse,
                membre.contact,
                membre.get_statut_display(),
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

        # Générer le PDF
        doc.build(elements)
        return response

    telecharger_rapport.short_description = "Télécharger la liste des membres sélectionnés (PDF)"





from django.utils.translation import gettext_lazy as _


admin.site.site_title= _('Admin VitalFit')
admin.site.site_header= _('Admin VitalFit')


