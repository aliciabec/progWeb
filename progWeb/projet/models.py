import datetime
from django.db import models
from django.utils import timezone

class Utilisateur(models.Model):
    email = models.EmailField(primary_key=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    mot_de_passe= models.CharField(max_length=30)
    tel = models.IntegerField()#max_length=30)
    role = models.CharField(max_length=100,choices=(("annot","annotateur"),("val", "validateur"),("user","utilisateur")),default="user")
    # Rajouter date et heure, il doit exister une fonction pour ça
    

class Genome(models.Model):
    Id_genome = models.CharField(max_length=100,primary_key=True)
    taille_sequence = models.CharField(max_length=100,blank=True,null=True)
    sequence_genome = models.TextField(null=True,blank=True)
    espece = models.CharField(max_length=100,null=True)

class Annotation(models.Model):
    Id_genome = models.ForeignKey(Genome,on_delete=models.CASCADE)#,primary_key=True)
    emailAnnotateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,null=True,related_name="emailAnnotateur")
    emailValidateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,null=True,related_name="emailValidateur")
    estValide = models.BooleanField(default=False)
    estAnnote = models.BooleanField(default=False)
    commentaire = models.CharField(max_length=1000000,null=True)

class Gene_prot(models.Model):
    nom_transcrit = models.TextField(max_length=100,primary_key=True)
    Id_genome = models.ForeignKey(Genome, on_delete=models.CASCADE) # clé etrangere de genome
    nom_gene = models.CharField(max_length=100, null = True)#,primary_key=True)
    start_position = models.IntegerField()#max_length=30)
    end_position = models.IntegerField()#max_length=30)
    description = models.CharField(max_length=1000000,null=True)
    sequence_nucleotidique = models.TextField(null=True)
    sequence_peptidique = models.TextField(null=True)
