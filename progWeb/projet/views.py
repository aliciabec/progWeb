from django.utils import timezone
from django.template import loader
### from .models import Choice, Question => c'est ici qu'il faudra importer les tables !!
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.template import RequestContext
from django.views import generic ### cette ligne nous permet d'avoir une classe qui va
### pouvoir nous donnée des type de list generic
### La vue générique DetailView s’attend à ce que la clé primaire capturée dans l’URL s’appelle "pk",
### nous avons donc changé question_id en pk pour les vues génériques.
from projet.models import Genome, Gene_prot, Annotation, Utilisateur
from projet.forms import MyForm
import pickle

def accueil(request):
    
    if request.method == 'POST':
        form = MyForm(request.POST)  

        ## Récuperation des infos 
        sequence = request.POST['seq']
        espece = request.POST['espece']
        nom_gene = request.POST['nom_gene']
        nom_transcrit = request.POST['nom_transcrit']
        description = request.POST['description']
        seq_prot = request.POST['seq_prot']

        ## Affichage test
        #print("TEST")
        #print(espece)
        #print(sequence)

        if form.is_valid():
            selected_value = 'r1/'

            if request.POST.get('my_field') == "r1" : 
                type_resultat="Genome"
                print("TEST")   

               
                qs = Genome.objects.values_list('Id_genome','taille_sequence', 'espece').filter(sequence_genome__contains=sequence).filter(espece=espece)
                
                ## On recupère les bons genomes grace aux requetes SQL
                for result in qs:
                    Id_genome = result[0]
                    espece_bd = result[2]

               


            # other_field_value = form.cleaned_data['other_field']
            # Traitement des données
                return HttpResponseRedirect(reverse('projet:r1'))

            elif request.POST.get('my_field') == "r2" : 
                type_resultat="Gene_prot"
            #    other_field_value = form.cleaned_data['other_field']
            # Traitement des données
                return HttpResponseRedirect(reverse('projet:r2'))

        ## Requetes SQL
       
        """
        elif type_resultat== "Gene_prot":

            Gene_prot.objects.all().filter(nom_transcrit = nom_transcrit,
            nom_gene = nom_gene ,sequence_peptidique = seq_prot, )
        """


    else:
        form = MyForm()

    return render(request, 'projet/accueil.html', {"form":form})




class Connexion(generic.ListView):
    template_name = 'projet/connexion.html'
    def get_queryset(self):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        print(self.request.user)
        return 0



class Inscription(generic.ListView):
    template_name = 'projet/inscription.html'
    def get_queryset(self):

        return 0
    
 
    def create_user(self):   
        ## test pour le role
        roles = ""
        print(self.GET)
        print(self.POST)
        print(self.POST.keys())
        if self.POST['roles'] == "lecteur":
            roles = 'user'
        elif self.POST['roles'] == "annotateur":
            roles = 'annot'
        elif self.POST['roles'] == "validateur":
            roles = 'val'
        Utilisateur(email = self.POST['email']
                    , nom = self.POST['nom']
                    , prenom= self.POST['prenom']
                    , mot_de_passe = self.POST['pass_word_id']
                    , tel = self.POST['tel']
                    , roles = roles).save()

        return HttpResponseRedirect('/projet/thanks/', RequestContext(self) )



class Annotation(generic.ListView):
    template_name = 'projet/annotation.html'
    def get_queryset(self):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        print(self.request.user)
        return 0



class Thanks(generic.ListView):
    template_name = 'projet/thanks.html'
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


class R1(generic.ListView):
    template_name = 'projet/r1.html'
    context_object_name = 'results_genomique'
    def get_queryset(self):
        return Genome.objects.all()

class R2(generic.ListView):
    template_name = 'projet/r2.html'
    context_object_name = 'results_gene_prot'
    def get_queryset(self):
        ## Maisen il faudra le modifier quand tu auras fait les requetes
        return Gene_prot.objects.filter(pk= 'AAN78501')