from django.db import models

class HIFKPelaaja(models.Model):
    nimi = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nimi

# Create your models here.
