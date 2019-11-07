from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import GuidelineForm
from .models import Guideline
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse

def guide_view(request): 
    if request.method == 'POST': 
        form = GuidelineForm(request.POST, request.FILES) 
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = GuidelineForm() 
    return render(request, 'upload.html', {'form' : form}) 
  
  
def success(request): 
    return HttpResponse('successfuly uploaded')

def display_guideline(request): 
  
    if request.method == 'GET': 
        guides = Guideline.objects.all()
        return render(request, 'display.html', {'guides' : guides})

def edit(request, id):
    guide = get_object_or_404(Guideline, pk=id)
    form = GuidelineForm(instance=guide) 

    if request.method == 'POST': 
        form = GuidelineForm(request.POST, request.FILES, instance=guide) 
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect(reverse('guideline:display'))

    return render(request, 'edit.html', {'guide': guide, 'form' : form}) 