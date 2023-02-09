from django.utils import timezone
from django.template import loader,RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic 
from projet.models import Genome, Gene_prot, Annotation, Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
import base64

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
                    , first_name= request.POST.get('prenom')
                    , password = request.POST.get('pass_word_id')
                    , tel = request.POST.get('tel')
                    , roles = role).save()
        return HttpResponseRedirect(reverse('projet:connexion'))
    else: 
        return render(request, 'projet/inscription.html')



class Annotation(generic.ListView):
    template_name = 'projet/annotation.html'
    def get_queryset(self):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        print(self.request.user)
        return 0


class Annot(generic.ListView):
    template_name = 'projet/annot.html'
    def get_queryset(self):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        print(self.request.user)
        return 0

def r1(request, requete):
    # Decode la requete
    requete_decode = json.loads(base64.b64decode(requete.encode("utf-8")).decode("utf-8"))

    # On initialise result avec tous les objects du Genome avec le filtre sur la sequence qui ne peut pas etre vide
    result = Genome.objects.filter(sequence_genome__contains=requete_decode['sequence'])
    # On filtre seulement si le champ est rempli par l'utilisateur
    # Pour le Genome seul le champ espece peut etre vide parmis les deux champs à remplir (sequence et espece)

    if requete_decode['espece']:
        result = result.filter(espece=requete_decode['espece'])

    
    for genome in result:
        # Reduce size for faster analysis
        genome.sequence_genome = genome.sequence_genome[0:int(len(genome.sequence_genome) /1000)] 

        genome_genes = Gene_prot.objects.filter(Id_genome=genome)
        
        list_genes = []

        for gene in genome_genes:
            start = gene.start_position
            end = gene.end_position
            nom_transcrit = gene.nom_transcrit
            sub_sequence = gene.sequence_nucleotidique
            list_genes.append({
                'start': start,
                'end': end,
                'nom_transcrit': nom_transcrit,
                'sub_sequence': sub_sequence
            })
        #start = genome_genes.objects.all()[:1].get()
        #print("TEST")
        #print(genome_genes)

        """
        start= 190
        start_temp = 1 # On commence à lire la sequence_genome par la position 1

        

        for i in range(start_temp, len(sequence_genome)):
            gene_dict = {}
            if i != start:
                gene_dict = {
                    sequence_genome[start_temp:start],
                    False
                }
                start_temp=start # On place le curseur au début du premier gene
            else:
                for gene in genome_genes:
                    start = gene.start_position
                    end = gene.end_position
                    nom_transcrit = gene.nom_transcrit
                    sub_sequence = gene.sequence_nucleotidique
                    gene_dict = {
                        sub_sequence,
                        start,
                        end,
                        nom_transcrit,
                        True
                    }
                    start_temp=end # On place le curseur à la fin du gene
        
            data.append(gene_dict)
        print(data)
    """
    return render(request, 'projet/r1.html', {'results_genomique': result,'list_genes': list_genes })


def separate_genes(dna_sequence, gene_length):
    genes = []
    for i in range(0, len(dna_sequence), gene_length):
        gene = dna_sequence[i:i + gene_length]
        genes.append(gene)
    return genes


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