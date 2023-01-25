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



class Connexion(generic.DetailView):
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
    def get(self, request):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        ## test pour le role 
        role = ""
        if request.POST['role'] == "lecteur":
            role = 'user'
        elif request.POST['role'] == "annotateur":
            role = 'annot'
        elif request.POST['role'] == "validateur":
            role = 'val'
        Utilisateur(email = request.POST['email-search']
                    , nom = request.POST['nom-search']
                    , prenom= request.POST['prenom-search']
                    , mot_de_passe = request.POST['pass_id-search']
                    , tel = request.POST['tel-search']
                    , role = role).save()

        return 0


class Annotation(generic.ListView):
    template_name = 'projet/annotation.html'
    def get_queryset(self):
#        """
##        Return the last five published questions (not including those set to be
#        published in the future).
#        """
        print(self.request.user)
        return 0
