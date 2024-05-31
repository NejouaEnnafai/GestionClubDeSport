from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import InscriptionForm 
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from .admin import *
from openpyxl import Workbook
from django.template.loader import get_template
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import Membre
from .forms import *
from .models import *
from .models import Evenement
from django.contrib.auth.decorators import user_passes_test
from .models import MembreEvenement
from SportClub.models import *


# Create your views here.

def authentification(request):
    error_message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('your_pass')
        if not User.objects.filter(username=username , password=password).exists:
          error_message = "Identifiants invalides. Veuillez réessayer."
        else:
              return redirect('index')

    return render(request, 'authentification.html', {'error_message': error_message})





def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
             error_message = "Le nom d'utilisateur existe déjà."
             return render(request, 'inscription.html', {'form': form, 'error_message': error_message})
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = form.save()    
            email = form.cleaned_data['email']
            subject = 'Bienvenue au VitaLift Club de Sport'
            message = """
Cher(e) membre,

Au nom de toute l'équipe du VitaLift Club de Sport, nous vous souhaitons la bienvenue !

Nous sommes ravis de vous accueillir parmi nos membres privilégiés. Votre santé et votre forme physique sont nos priorités, et nous sommes déterminés à vous offrir les meilleurs services.

Notre équipe d'entraîneurs et de professionnels qualifiés est là pour vous guider dans votre parcours sportif. Que ce soit pour des séances d'entraînement, des cours de groupe ou des conseils personnalisés, nous sommes là pour répondre à vos besoins.

N'hésitez pas à parcourir notre site web pour découvrir nos offres, consulter les horaires de nos activités et accéder à des informations utiles pour votre pratique sportive. Nous avons conçu ce site dans le but de vous offrir une expérience conviviale et informative.

Si vous avez des questions, des préoccupations ou besoin d'assistance, notre équipe dédiée est à votre disposition. Nous sommes là pour vous aider à atteindre vos objectifs et à profiter pleinement de votre adhésion.

Nous sommes honorés de pouvoir contribuer à votre bien-être et nous espérons que votre expérience avec nous sera exceptionnelle. Nous avons hâte de vous rencontrer au VitaLift Club de Sport.

Avec nos salutations sportives,
L'équipe du VitaLift Club de Sport
"""
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            # Ajoutez ici le code supplémentaire que vous souhaitez exécuter après l'inscription réussie
            messages.success(request, "Inscription réussie !")
            # Connecter automatiquement l'utilisateur après l'inscription
            user.save()
            # Rediriger vers une autre page après l'inscription réussie
            return render(request, 'inscripEffect.html')
        
    else:
        form = InscriptionForm()
        context = {
    'form': form
}
    return render(request, 'inscription.html', {'form': form})



def about(request):
    # Récupérez tous les événements depuis la base de données
    evenements = Evenement.objects.all()
    
    # Vous pouvez également trier les événements si nécessaire
    # evenements = Evenement.objects.order_by('date')
    
    context = {
        'evenements': evenements
    }
    
    return render(request, 'about.html', context)






def contact(request):
       # Récupérez tous les événements depuis la base de données
    ressources_equipement = Ressource.objects.filter(type='equipement', disponibilite=True)
    
    context = {
        'ressources_equipement': ressources_equipement
    }
    
    return render(request, 'contact.html', context)











def inscriEvent(request):
    
    evenements = Evenement.objects.all()
    form = InscriptionEventForm(request.POST or None, evenements=Evenement.objects.all())

    if request.method == 'POST' and form.is_valid():
        nom = form.cleaned_data['nom']
        prenom = form.cleaned_data['prenom']
        event_id = int(request.POST.get('evenement_pk'))

        try:
            membre = Membre.objects.get(nom=nom, prenom=prenom)
        except Membre.DoesNotExist:
            messages.error(request, "Le membre n'existe pas. Veuillez vérifier le nom et prénom.")
            return redirect('inscriEvent')

        if MembreEvenement.objects.filter(membre=membre, evenement_id=event_id).exists():
            messages.error(request, "Vous êtes déjà inscrit à cet événement.")
        else:
            MembreEvenement.objects.create(membre=membre, evenement_id=event_id)
            messages.success(request, "Inscription réussie !")

    return render(request, 'inscriEvent.html', {'evenements': evenements, 'form': form})

def index(request):
   if request.method == 'POST':
        # Get form data from POST request
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Compose and send the email
        subject = f"New Contact Form Submission from {fname} {lname}"
        sender_mail = email  # Replace with your email
        recipient_list = ['VitaLiftClub@gmail.com']  # List of recipient email addresses
        message_body = f"Nom: {fname}\nPrénom: {lname}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(subject, message_body,sender_mail, recipient_list, fail_silently=False)

        # Display a success message in the view
        success_message = "Votre message a été bien reçu, nous vous contacterons bientôt."

        # Render the contact form template with the success message
        return render(request, 'index.html', {'success_message': success_message})
    
   return render(request, 'index.html')



def inscripEffect(request):
    template = loader.get_template('inscripEffect.html')
    return HttpResponse(template.render())

def service(request):
    # Récupérez tous les événements depuis la base de données
    activites = Activite.objects.all()
    
    # Vous pouvez également trier les événements si nécessaire
    # evenements = Evenement.objects.order_by('date')
    
    context = {
        'activites': activites
    }
    
    return render(request, 'service.html', context)
    
    

def inscriActi(request):
    
    Activites = Activite.objects.all()
    form = InscriptionActiForm(request.POST or None, Activites=Activite.objects.all())

    if request.method == 'POST' and form.is_valid():
        nom = form.cleaned_data['nom']
        prenom = form.cleaned_data['prenom']
        Activite_id = int(request.POST.get('Activite_pk'))

        try:
            membre = Membre.objects.get(nom=nom, prenom=prenom)
        except Membre.DoesNotExist:
            messages.error(request, "Le membre n'existe pas. Veuillez vérifier le nom et prénom.")
            return redirect('inscriActi')

        if MembreActivite.objects.filter(membre=membre, activite_id=Activite_id).exists():
            messages.error(request, "Vous êtes déjà inscrit à cet événement.")
        else:
            MembreActivite.objects.create(membre=membre, activite_id=Activite_id)
            messages.success(request, "Inscription réussie !")

    return render(request, 'inscriActi.html', {'Activites': Activites, 'form': form})









def envoyer_email_adhesion_expire(membre):
    sujet = "Votre adhésion expire bientôt"
    message = f"Cher(e) {membre.nom},\n\nVotre adhésion au club expire le {membre.adhesion.date_fin}. Veuillez renouveler votre adhésion pour continuer à profiter de nos services.\n\nCordialement, L'équipe du club"
    de = settings.EMAIL_HOST_USER  # Adresse e-mail de l'expéditeur
    destinataires = [membre.email]

    send_mail(sujet, message, de, destinataires, fail_silently=False)

def verifier_adhesion_expire():
    membres = Membre.objects.all()

    for membre in membres:
        if membre.adhesion.date_fin <= timezone.now().date():
            envoyer_email_adhesion_expire(membre)






from xhtml2pdf import pisa

def generate_pdf(request):
    # Générez le rapport ici (par exemple, au format HTML)
    # Utilisez des bibliothèques telles que ReportLab ou xhtml2pdf pour générer le contenu du rapport au format PDF.

    # Exemple de génération d'un modèle HTML pour le rapport PDF
    template_path = 'rapport_membres_template.html'
    context = {
        'membres': Membre.objects.all()  # Ajoutez les données des membres nécessaires ici
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_membres.pdf"'

    # Chargez le modèle HTML
    template = get_template(template_path)
    html = template.render(context)

    # Générez le PDF à partir du modèle HTML
    pisaStatus = pisa.CreatePDF(html, dest=response)

    if pisaStatus.err:
        return HttpResponse('Erreur lors de la génération du PDF', content_type='text/plain')

    return response



from .forms import ReservationForm
from datetime import datetime, time,timedelta



def inscriRes(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            ressource = form.cleaned_data['ressource']
            date = form.cleaned_data['date']
            heure = form.cleaned_data['heure']
            nom_membre = form.cleaned_data['nom_membre']
            prenom_membre = form.cleaned_data['prenom_membre']

            try:
                membre = Membre.objects.get(nom=nom_membre, prenom=prenom_membre)
            except Membre.DoesNotExist:
                messages.error(request, "Le membre n'existe pas. Veuillez vérifier le nom et prénom.")
                return render(request, 'inscriRes.html', {'form': form})

            heure_debut = datetime.combine(date, heure)
            heure_fin = heure_debut + timedelta(hours=1)

            # Vérifiez si l'heure de début est entre 8h et 22h
            heure_limite_debut = time(8, 0)
            heure_limite_fin = time(22, 0)

            if heure_debut.time() < heure_limite_debut or heure_debut.time() >= heure_limite_fin:
                messages.error(request, 'Les réservations ne sont autorisées qu\'entre 8h et 22h.')
                return render(request, 'inscriRes.html', {'form': form})

            reservations_exist = Reservation.objects.filter(
                ressource=ressource,
                date=date,
                heure__range=(heure_debut.time(), heure_fin.time())
            ).exists()

            if not reservations_exist:
                reservation = Reservation(
                    ressource=ressource,
                    date=date,
                    heure=heure_debut.time(),
                    membre=membre
                )
                reservation.save()

                # Ajoutez un message flash pour indiquer que la réservation a été effectuée
                messages.success(request, 'Réservation effectuée avec succès!')

                return redirect('inscriRes')
            else:
                messages.error(request, 'La ressource est déjà réservée à cette heure.')
    else:
        form = ReservationForm()

    ressources_disponibles = Ressource.objects.filter(type='equipement')

    return render(request, 'inscriRes.html', {'form': form, 'ressources_disponibles': ressources_disponibles})




