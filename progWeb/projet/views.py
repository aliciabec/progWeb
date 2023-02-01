from django.utils import timezone
from django.template import loader,RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic 
from projet.models import Genome, Gene_prot, Annotation, Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
import base64

import pickle

def accueil(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    
    if request.method == 'POST':
        
        if len(request.POST.get('seq')) < 3:
            # Message d'erreur si l'utilisateur rentre un nombre de nucléotide inférieur à 3.
            messages.add_message(request, messages.ERROR, 'Au moins trois caractères sont nécessaires dans la séquence.')
            return render(request, 'projet/accueil.html')

        if not request.POST.get('type_recherche'):
            # Message d'erreur si l'utilisateur ne coche aucune des cases
            messages.add_message(request, messages.ERROR, 'Veuillez cocher au moins une des cases ci-dessous (Genome ou Gene/proteine).')
            return render(request, 'projet/accueil.html')

        if request.POST.get('type_recherche') == "genome" :
            requete = {}
            requete['sequence'] = request.POST.get('seq')
            requete['espece'] = request.POST.get('espece')
            # Encode the JSON string with base64
            requete_encode = base64.b64encode(json.dumps(requete).encode("utf-8"))

            return HttpResponseRedirect(reverse('projet:r1', args=(requete_encode.decode("utf-8"),)))

        elif request.POST.get('type_recherche') == "gene_prot" :
            requete = {}
            requete['sequence'] = request.POST.get('seq')
            requete['espece'] = request.POST.get('espece')
            requete['nom_gene'] = request.POST.get('nom_gene')
            requete['nom_transcrit'] = request.POST.get('nom_transcrit')
            requete['description'] = request.POST.get('description')
            requete['seq_proteine'] = request.POST.get('seq_prot')

            # Encode the JSON string with base64
            requete_encode = base64.b64encode(json.dumps(requete).encode("utf-8"))

            return HttpResponseRedirect(reverse('projet:r2', args=(requete_encode.decode("utf-8"),)))

    else:
        return render(request, 'projet/accueil.html',{"user": user})


def connexion(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('pass_word_id')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('projet:accueil'))
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            messages.add_message(request, messages.ERROR, 'Incorrect username or password.')
            return render(request, 'projet/connexion.html')

    else:
        # The request is not a POST, so display the login form.
        # This scenario would most likely be a GET.
        return render(request, 'projet/connexion.html')


def inscription(request): 
    if request.method == 'POST':
        ## Etapes de recuperation de la valeur de role  

        role = 'user'
        if request.POST.get('roles') == "lecteur":
            role = 'user'
        elif request.POST.get('roles') == "annotateur":
            role = 'annot'
        elif request.POST.get('roles') == "validateur":
            role = 'val'

        ## Creation de l'utlisateur avec les informations rentrees par l'utilisateur 
        Utilisateur.objects.create_user(username = request.POST.get('username')
                    , email = request.POST.get('email')
                    , last_name = request.POST.get('nom')
                    , first_name = request.POST.get('prenom')
                    , password = request.POST.get('pass_word_id')
                    , tel = request.POST.get('tel')
                    , roles = role).save()
        return HttpResponseRedirect(reverse('projet:connexion'))
    else: 
        return render(request, 'projet/inscription.html')


def annotation(request, pk):
    annotation = get_object_or_404(Annotation, pk=pk)
    ### cet object va recupere tout ce qui possède le meme Id_genome que l'annotation dans la classe gene_prot
    id_genome = annotation.Id_genome.Id_genome
    gene_prot_id_genome = Gene_prot.objects.filter(Id_genome = id_genome)
    
    if request.method == 'POST':
        
        # Rajoute dans la base les genes si l'utilsateur clique sur le bouton annot_gene
        # Va renvoyer un message d'erreur si tout les cadres ne sont pas completé
        if request.POST.get('gene_p') \
            and request.POST.get('nom_gene') \
            and request.POST.get('description') \
            and request.POST.get("annot_gene"): 

            gene_prot = gene_prot_id_genome.filter(nom_transcrit = request.POST.get('gene_p'))[0]
            gene_prot.nom_gene = request.POST.get('nom_gene')
            gene_prot.description = request.POST.get('description')
            gene_prot.save()
        else : 
            messages.add_message(request, messages.ERROR, 'Nom du gene ou/et description vide.')

        # On rajoute dans la base de genome si on a cliquer sur le bouton annotation
        # puis on verifie les condition d'annotation.
        # On mets un message d'erreurs si on clique sur le bouton annotation est que 
        # toutes les informations ne sont pas rentre.
        if request.POST.get('fin_annotation'):
            if request.POST.get('espece'):
                genome_selected = Genome.objects.get(Id_genome = id_genome)
                genome_selected.espece = request.POST.get('espece')
                genome_selected.save()

            annotation.estAnnote = True
            for gene in gene_prot_id_genome:
                if gene.description == None or gene.nom_gene == None or Genome.objects.get(Id_genome = id_genome).espece == None:
                    annotation.estAnnote = False
            annotation.save()
            if annotation.estAnnote:
                return HttpResponseRedirect(reverse('projet:annot'))
            else: 
                messages.add_message(request, messages.ERROR, 'Tous les genes n\'ont pas été annoté.')

            
    ### ici on va renvoyer les annotations pour avoir Id_genome, les gene_prot selectionne pour avoir les genes 
    ### mais notamment gene_json qui est une conversion de gene_prot en json pour l'utliser dans le javascript
    return render(request, 'projet/annotation.html', context={'annotation': annotation, 'gene_prot':gene_prot_id_genome
        , 'gene_json' :json.dumps(list(gene_prot_id_genome.values()),default=str)}) 
    

def annotvisu(request, pk):
    annotation = get_object_or_404(Annotation, pk=pk)
    id_genome = annotation.Id_genome.Id_genome
    gene_prot_id_genome = Gene_prot.objects.filter(Id_genome = id_genome)
    
    
    if request.method == 'POST':
        user = None
        if request.user.is_authenticated:
            user = request.user
        
        if request.POST.get('Validation'):
            annotation.estValide = True
            annotation.save()
            return HttpResponseRedirect(reverse('projet:annot'))


    return render(request, 'projet/annotvisu.html'
        , context={'annotation' : annotation
        , 'gene_prot':gene_prot_id_genome
        , 'gene_json' :json.dumps(list(gene_prot_id_genome.values()),default=str)
        , 'genome' : Genome.objects.get(pk = id_genome)}) 


def annot(request):
    annotation = Annotation.objects.filter(estAnnote = False)
    annotationAnnote = Annotation.objects.filter(estAnnote = True)
    try:
        user = None
        if request.user.is_authenticated:
                user = request.user
    except AttributeError:
        print("Aucun utilisateur n'est connecter. Revenez sur la page d'accueil.")

    if request.method == 'POST':
        
        for annot in annotationAnnote:
            
            if request.POST.get('button_' + str(annot.id) + '_annot'):
                return HttpResponseRedirect(reverse('projet:annotvisu', args=(annot.id,)))

        for annot in annotation:

            if request.POST.get('button_' + str(annot.id) + '_not_annot'):
            
                a = annotation.get(id = annot.id)
                a.emailAnnotateur = Utilisateur.objects.get(username = request.POST.get(str(annot.id)))
                a.emailValidateur = Utilisateur.objects.get(username = user.username)
                a.save()         

            elif request.POST.get('button_' + str(annot.id) + '_annotateur_def'):
                
                return HttpResponseRedirect(reverse('projet:annotation', args=(annot.id,))) 
        
    return render(request, 'projet/annot.html', 
            context={'liste_annot': Utilisateur.objects.filter(roles='annot')
                    ,'annotationNonAnnote' : annotation.filter(emailAnnotateur = None, emailValidateur = None)
                    ,'annotationAttribue' : annotation.exclude(emailAnnotateur = None, emailValidateur = None)
                    , 'annotationAnnote' : annotationAnnote}) 



def r1(request, requete):
    # Decode la requete
    requete_decode = json.loads(base64.b64decode(requete.encode("utf-8")).decode("utf-8"))

    # On initialise result avec tous les objects du Genome avec le filtre sur la sequence qui ne peut pas etre vide
    result = Genome.objects.filter(sequence_genome__contains=requete_decode['sequence'])
    print("TEST")
    print(result)

    # On filtre seulement si le champ est rempli par l'utilisateur
    # Pour le Genome seul le champ espece peut etre vide parmis les deux champs à remplir (sequence et espece)

    if requete_decode['espece']:
        result = result.filter(espece=requete_decode['espece'])
 
    return render(request, 'projet/r1.html', {'results_genomique': result})

def r2(request, requete):
    # Decode la requete
    requete_decode = json.loads(base64.b64decode(requete.encode("utf-8")).decode("utf-8"))

    # On initialise result avec tous les objects du Gene_prot avec le filtre sur la sequence qui ne peut pas etre vide
    result = Gene_prot.objects.filter(sequence_nucleotidique__contains=requete_decode['sequence'])

    # On filtre seulement si le champ est rempli par l'utilisateur

    if requete_decode['nom_gene']:
        result = result.filter(nom_gene=requete_decode['nom_gene'])
        
    if requete_decode['nom_transcrit']:
        result = result.filter(nom_transcrit= requete_decode['nom_transcrit'])
        
    if requete_decode['seq_proteine']:
        result=result.filter(sequence_peptidique__contains=requete_decode['seq_proteine'])
            
    if requete_decode['description']:
        result=result.filter(description__contains=requete_decode['description'])

    return render(request, 'projet/r2.html', {'results_gene_prot': result})