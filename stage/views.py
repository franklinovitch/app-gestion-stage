# -*- coding: utf-8 -*-
# Create your views here.
from stage.models import Stage
from stage.forms import StageForm, supprimeStageForm
from django.shortcuts import HttpResponseRedirect, HttpResponse
from gestionStage.shortcuts import render
from django.forms import ModelForm
from django.template import RequestContext
from django.core.context_processors import csrf
#from stage.forms import supprimeStageForm

def show_stages(request):
	return render(
		request,
		"stage/stage.html",
		{"liste_stage": Stage.objects.order_by("intitule")})

def show_detail_stage(request, pk):
	return render(
		request,
		"stage/detail_stage.html",
		{"stage": Stage.objects.get(pk=pk)}
		)

# Manipulation Entreprise
def addStage(request):
	#entreprise_form = EntrepriseForm()
	#form = EntrepriseForm(instance=Entreprise.objects.all()[1])

	if request.method == 'POST':  # S'il s'agit d'une requête POST
		form = StageForm(request.POST)  # Nous reprenons les données

		if form.is_valid(): # Nous vérifions que les données envoyées sont valides
			form.save()
			return HttpResponseRedirect('/stage')

	form = StageForm()  # Nous créons un formulaire vide
	con = { 'actionAFaire' : 'Ajouter', 'form' : form}

	return render(request,'stage/forms.html',
							con)
	#return render(request, 'addEnt.html', locals())

def modifStage(request, pk):
	if request.method == 'POST':  # S'il s'agit d'une requête POST
		form = StageForm(request.POST,instance=Stage.objects.get(pk=pk))
		if form.is_valid(): # Nous vérifions que les données envoyées sont valides
			form.save()
			return HttpResponseRedirect('/stage/' + pk)
	else: # Si ce n'est pas du POST, c'est probablement une requête GET
		form = StageForm(instance=Stage.objects.get(pk=pk))
		print("Error")
		  # Nous créons un formulaire vide

	return render(request,'stage/forms.html', 
							{ 'actionAFaire' : 'Modifier', 'form' : form})


def delStage(request):
 
    supprimestageform = supprimeStageForm()
    con ={'form': supprimestageform, 'actionAFaire' : 'Supprimer'}
    con.update(csrf(request))
    if len(request.POST) > 0:
        supprimestageform =supprimeStageForm(request.POST)
        con = {'form': supprimestageform}
        if supprimestageform.is_valid():  
            supprimestageform.save()
            return HttpResponseRedirect("/stage/")
    else:
        return render(request,'stage/forms.html', con)