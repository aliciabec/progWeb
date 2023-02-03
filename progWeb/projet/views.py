from django.utils import timezone
from django.template import loader,RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic 
from projet.models import Genome, Gene_prot, Annotation, Utilisateur
from django.contrib.auth import authenticate, login
from django.contrib import messages
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