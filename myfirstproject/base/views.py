from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Space, Heading
from .forms import SpaceForm

# Create your views here.


# spaces = [
#     {'id':1, 'name':'Let learn the django'},
#     {'id':2, 'name':'Vishesh is going to design the page'},
#     {'id':3, 'name':'Backend developers'},
#     {'id':4, 'name':'Frontend developers'},
# ]


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exist')

        user = authenticate(request, username=username, password=password)   

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Username or Password does Not Exist')


    context = {}
    return render(request, 'base/login_register.html', context)





def home(request):

 q = request.GET.get('q') if request.GET.get('q') != None else ''

 spaces = Space.objects.filter(
    Q(heading__name__icontains=q) | 
    Q(name__icontains=q) | 
    Q(description__icontains=q) 
    )


 headings = Heading.objects.all()
 space_count = spaces.count()

 context = {'spaces': spaces, 'headings': headings, 'space_count': space_count}
 return render(request, 'base/home.html', context)


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


def deleteSpace(request, pk):
    space = Space.objects.get(id=pk)
    if request.method == 'POST':
        space.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':space})