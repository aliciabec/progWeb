from django.utils import timezone
from django.template import loader
### from .models import Choice, Question => c'est ici qu'il faudra importer les tables !!
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic ### cette ligne nous permet d'avoir une classe qui va
### pouvoir nous donnée des type de list generic
### La vue générique DetailView s’attend à ce que la clé primaire capturée dans l’URL s’appelle "pk",
### nous avons donc changé question_id en pk pour les vues génériques.
from projet.models import Genome, Gene_prot, Annotation, Utilisateur



class Accueil(generic.ListView):
    template_name = 'projet/accueil.html'
    def get_queryset(self):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        print(self.request.user)
        return 0



class Connexion(generic.ListView):
    template_name = 'projet/connexion.html'
    def get_queryset(self):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        print(self.request.user)
        return 0

from django.template import RequestContext


class Inscription(generic.ListView):
    template_name = 'projet/inscription.html'
    def get_queryset(self):
#        
##       Return the last five published questions (not including those set to be
#        published in the future).
#      
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
