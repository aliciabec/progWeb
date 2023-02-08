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


def accueil(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    
    if request.method == 'POST':
       
        if request.POST.get('type_recherche') == "genome" :
            requete = {}
            requete['sequence'] = request.POST.get('seq')
            requete['espece'] = request.POST.get('espece')

            # Encode the JSON string with base64
            requete_encode = base64.b64encode(json.dumps(requete).encode("utf-8"))

            return HttpResponseRedirect(reverse('projet:r1', args=(requete_encode.decode("utf-8"),)))
        elif request.POST.get('type_recherche') == "gene_prot" :
            return HttpResponseRedirect(reverse('projet:r2'))
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
        if request.POST.get('gene_p') and request.POST.get('nom_gene') and request.POST.get('description'): 
            gene_prot = gene_prot_id_genome.filter(nom_transcrit = request.POST.get('gene_p'))[0]
            gene_prot.nom_gene = request.POST.get('nom_gene')
            gene_prot.description = request.POST.get('description')
            gene_prot.save()
        else : 
            messages.add_message(request, messages.ERROR, 'Nom du gene ou/et description vide.')

        if not request.POST.get('fin_annotation'):
            ### boucle qui va nous permettre de mettre a jour la variable estAnnot ou non l'annotation
            if request.POST.get('espece'):
                genome_selected = Genome.objects.get(Id_genome = id_genome)
                genome_selected.espece = request.POST.get('espece')
                genome_selected.save()
            else : 
                messages.add_message(request, messages.ERROR, 'Il n\'y a pas de nom d\'espece.')

            annotation.estAnnote = True
            for gene in gene_prot_id_genome:
                if gene.description == None or gene.nom_gene == None or Genome.objects.get(Id_genome = id_genome).espece == None:
                    annotation.estAnnote = False

            if annotation.estAnnote:
                return HttpResponseRedirect(reverse('projet:annot'))
            else: 
                messages.add_message(request, messages.ERROR, 'Tous les genes ne sont pas annoté.')

    return render(request, 'projet/annotation.html', context={'annotation': annotation, 'gene_prot':gene_prot_id_genome
        , 'gene_json' :json.dumps(list(gene_prot_id_genome.values()),default=str)}) 
    ### ici on va renvoyer les annotations pour avoir Id_genome, les gene_prot selectionne pour avoir les genes 
    ### mais notamment gene_json qui est une conversion de gene_prot en json pour l'utliser dans le javascript


class Annot(generic.ListView):
    template_name = 'projet/annot.html'
    context_object_name = 'liste_annot'
    def val_or_annot(request):
        user = None
        if request.user.is_authenticated:
            user = request.user
    def get_queryset(self):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        #print(self.request.user)
        return Utilisateur.objects.filter(roles='annot')


#class R1(generic.ListView):
#    template_name = 'projet/r1.html'
#    context_object_name = 'results_genomique'
#    def get_queryset(self, requete):
#        return requete

def r1(request, requete):
    # Decode la requete
    requete_decode = json.loads(base64.b64decode(requete.encode("utf-8")).decode("utf-8"))
    qs = Genome.objects.filter(sequence_genome__contains=requete_decode['sequence']).filter(espece=requete_decode['espece'])
    return render(request, 'projet/r1.html', {'results_genomique': qs})

class R2(generic.ListView):
    template_name = 'projet/r2.html'
    context_object_name = 'results_gene_prot'
    def get_queryset(self):
        ## Maisen il faudra le modifier quand tu auras fait les requetes
        return Gene_prot.objects.filter(pk= 'AAN78501')