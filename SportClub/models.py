from django.db import models

# Create your models here.

class Membre(models.Model):
    STATUT_CHOICES = (
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('entraineur', 'Entraîneur'),
        ('benevole', 'Bénévole'),
        # Ajoutez d'autres statuts ici
    )

    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField()  
    adresse = models.TextField()
    contact = models.CharField(max_length=20)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    


from django.utils import timezone

class Adhesion(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date_debut = models.DateField(default=timezone.now)
    date_fin = models.DateField()
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Adhesion de {self.membre} du {self.date_debut} au {self.date_fin}"
    


class Activite(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    heure = models.TimeField()
    lieu = models.CharField(max_length=100 , default='Club VitalFit ,12 Rue des Palmiers, Quartier des Fleurs, Casablanca, Maroc')
    affiche = models.ImageField(upload_to='activite_affiches/', default='full-shot-woman-doing-sport.jpg')

    def __str__(self):
        return self.nom
    


class MembreActivite(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.membre} participe à {self.activite}"
    


class Evenement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    heure = models.TimeField()
    lieu = models.CharField(max_length=100)
    affiche = models.ImageField(upload_to='evenement_affiches/')

    def __str__(self):
        return self.nom
    

class MembreEvenement(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.membre} participe à {self.evenement}"
    

class Ressource(models.Model):
    TYPE_CHOICES = (
        ('installation', 'Installation'),
        ('equipement', 'Équipement'),
        ('stock', 'Stock'),
        
    )

    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    disponibilite = models.BooleanField(default=True)
    equipement = models.ImageField(upload_to='equipement_photo/', default='poids-haltere-fonte.jpg')

    def __str__(self):
        return self.nom
    

class Reservation(models.Model):
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)

    def __str__(self):
        return f"Réservation de {self.ressource} par {self.membre} le {self.date} à {self.heure}"