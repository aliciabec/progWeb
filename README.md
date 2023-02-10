# Projet_Web Django

Notre projet Web consiste à l’élaboration d’un site internet permettant la recherche de génome/gènes dans une base de données et permettant également l’annotation de nouveau génome.Ce projet a été réalisé avec le framework Django qui sert de web service.

***ETAPE 1: Installation des packages***

Les packages nécessaires au projet sont présents dans le fichier requirements.txt. 

***ETAPE 2: Création de la base de donnée***

Pour créer la base de donnée, allez dans le répertoire progWeb/ qui contient le fichier manage.py puis exécutez les commandes suivantes:

 ```
    python manage.py makemigrations projet
 ```
 ```
    python manage.py sqlmigrate projet 0001
 ```
 ```
    python manage.py migrate
 ```
 ```
    echo 'import projet.parsing.py' | python manage.py shell
 ```
Vous pouvez vérifier que votre base est correctement rempli directement dans votre shell:

 ```
    python manage.py shell
 ```
 
Vous devez importer vos tables avec la commande suivante:

```
    from projet.models import Genome, Gene_prot, Annotation, Utilisateur
```
Puis regarder ce que contient l'une de votre table, par exemple la table Génome:

```
    Genome.objects.all()
```

***ETAPE 3: Lancer le site internet***

Pour lancer le site internet, il faut lancer la commande suivante:

```
    python manage.py runserver
```
Attention à bien etre situé dans vos dossiers (à l'endroit ou se situe le fichier manage.py).

Pour arriver sur la page connexion, il vous suffit d'aller à l'URL suivante:

http://127.0.0.1:8000/projet/connexion

Une fois arrivé sur la page de connexion vous pourrez naviguer sur l'ensemble du site.
