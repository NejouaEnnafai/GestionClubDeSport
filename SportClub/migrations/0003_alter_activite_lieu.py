# Generated by Django 4.0.10 on 2023-09-07 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportClub', '0002_activite_affiche'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activite',
            name='lieu',
            field=models.CharField(default='Champ de Mars, 5 Av. Anatole France, 75007 Paris, France', max_length=100),
        ),
    ]
