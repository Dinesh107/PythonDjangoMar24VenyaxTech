from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Space
from .forms import SpaceForm

# Create your views here.


# spaces = [
#     {'id':1, 'name':'Let learn the django'},
#     {'id':2, 'name':'Vishesh is going to design the page'},
#     {'id':3, 'name':'Backend developers'},
#     {'id':4, 'name':'Frontend developers'},
# ]


def home(request):
 spaces = Space.objects.all()
 return render(request, 'base/home.html', {'spaces':spaces})

 
def space(request, pk):   
 space = Space.objects.get(id=pk) 
 context = {'space': space}        
 return render(request, 'base/space.html', context)


def takingPhoto(request):
    return render(request, 'takingPhoto.html')


def createSpace(request): 
    form = SpaceForm()

    if request.method == 'POST':
       form = SpaceForm(request.POST)
       if form.is_valid():
        form.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/space_form.html', context)
 


def updateSpace(request, pk):
        space = Space.objects.get(id=pk)
        form = SpaceForm(instance=space)

        if request.method == 'POST':
            form = SpaceForm(request.POST, instance=space)
            if form.is_valid():
                form.save()
                return redirect('home')

        context = {'form': form}
        return render(request, 'base/space_form.html', context)

