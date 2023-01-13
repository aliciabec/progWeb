import datetime
from django.db import models
from django.utils import timezone

class Test(models.Model):
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text


class Utilisateur(models.Model):
    email = models.CharField(max_length=100,primary_key=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    mot_de_passe= models.CharField(max_length=30)
    tel = models.IntegerField(max_length=30)
    # Rajouter date et heure, il doit exister une fonction pour ça

class Annotateur(models.Model):
    email = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

class Validateur(models.Model):
    email = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
 

class Genome(models.Model):
    Id_genome = models.CharField(max_length=100,primary_key=True)
    contenu_genome = models.CharField(max_length=10000000)
    email = models.ForeignKey(Utilisateur, on_delete=models.CASCADE) # clé etrangere de utilisateur

class Gene(models.Model):
    Id_genome = models.ForeignKey(Genome, on_delete=models.CASCADE) # clé etrangere de utilisateur de genome

class Annotaté(models.Model):
    Id_genome = models.ForeignKey(Genome, on_delete=models.CASCADE) # clé etrangere de genome
    espece = models.CharField(max_length=100)

class Attribué(models.Model):
    Id_genome = models.ForeignKey(Genome, on_delete=models.CASCADE) # clé etrangere de genome
    email_annot = models.CharField(max_length=100)
    email_valid = models.CharField(max_length=100)
    validé = #true ou false
    commentaire = models.CharField(max_length=1000000)

class Chaine_prot(models.Model):
    Id_genome = models.ForeignKey(Genome, on_delete=models.CASCADE) # clé etrangere de genome
    nom_gene = models.CharField(max_length=100,primary_key=True)
    description = models.CharField(max_length=1000000)

class Gene(models.Model):
    Id_genome = models.ForeignKey(Genome, on_delete=models.CASCADE) # clé etrangere de genome
    nom_gene = models.CharField(max_length=100,primary_key=True)
    start_position = models.IntegerField(max_length=30)
    end_position = models.IntegerField(max_length=30)
    sequence_nucleotidique = models.CharField(max_length=10000000)


class proteine(models.Model):
    Id_genome = models.ForeignKey(Genome, on_delete=models.CASCADE) # clé etrangere de genome
    nom_gene = models.CharField(max_length=100,primary_key=True)
    start_position = models.IntegerField(max_length=30)
    end_position = models.IntegerField(max_length=30)
    sequence_peptidique = models.CharField(max_length=10000000)