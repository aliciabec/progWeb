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

def accueil(request):
    selected_value = ""
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            selected_value = 'r1/'

            if request.POST.get('my_field') == "r1" : 

            #    other_field_value = form.cleaned_data['other_field']
            # Traitement des données
                return HttpResponseRedirect(reverse('projet:r1'))
            elif request.POST.get('my_field') == "r2" : 

            #    other_field_value = form.cleaned_data['other_field']
            # Traitement des données
                return HttpResponseRedirect(reverse('projet:r2'))
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