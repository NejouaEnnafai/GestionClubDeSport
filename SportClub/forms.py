from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import admin






class InscriptionForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
       
            'first_name': forms.TextInput(attrs={'placeholder': 'Votre nom'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Votre prénom'}),
            'username': forms.TextInput(attrs={'placeholder': 'Votre nom d\'utilisateur'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Votre email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Votre mot de passe'}),
            
        

        }
        
class InscriptionEventForm(forms.Form):
    nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input-text'}))
    prenom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input-text', 'required': 'true'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input-text', 'required': 'true', 'pattern': '[^@]+@[^@]+\.[a-zA-Z]{2,6}'}))
#evenement_pk = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'input-text'}))
    evenement_pk = forms.ModelChoiceField(queryset=Evenement.objects.all(), empty_label="Sélectionnez un événement")
    
    
    def __init__(self, *args, **kwargs):
        evenements = kwargs.pop('evenements', [])
        super(InscriptionEventForm, self).__init__(*args, **kwargs)
        self.fields['evenement_pk'].choices = [(str(evenement.id), evenement.nom) for evenement in evenements]



class InscriptionActiForm(forms.Form):
    nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input-text'}))
    prenom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input-text', 'required': 'true'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input-text', 'required': 'true', 'pattern': '[^@]+@[^@]+\.[a-zA-Z]{2,6}'}))
    Activite_pk = forms.ModelChoiceField(queryset=Activite.objects.all(), empty_label="Sélectionnez une activité")

    def __init__(self, *args, **kwargs):
        Activites = kwargs.pop('Activites', [])
        super(InscriptionActiForm, self).__init__(*args, **kwargs)
        self.fields['Activite_pk'].choices = [(str(Activite.id), Activite.nom) for Activite in Activites]







class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['ressource', 'date', 'heure']
        widgets = {
            'ressource': forms.Select(attrs={'class': 'input-text'}),
            'date': forms.DateInput(attrs={'class': 'input-text', 'type': 'date'}),
            'heure': forms.TimeInput(attrs={'class': 'input-text', 'type': 'time'}),
        }

    # Ajoutez un champ pour la recherche du membre par nom et prénom
    nom_membre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input-text'}))
    prenom_membre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input-text'}))

