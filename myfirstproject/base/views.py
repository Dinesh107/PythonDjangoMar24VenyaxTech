from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Space, Heading, Communicate
from .forms import SpaceForm

# Create your views here.


# spaces = [
#     {'id':1, 'name':'Let learn the django'},
#     {'id':2, 'name':'Vishesh is going to design the page'},
#     {'id':3, 'name':'Backend developers'},
#     {'id':4, 'name':'Frontend developers'},
# ]


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')    
    
    return render(request, 'base/login_register.html', {'form': form})

def home(request):

 q = request.GET.get('q') if request.GET.get('q') != None else ''

 spaces = Space.objects.filter(
    Q(heading__name__icontains=q) | 
    Q(name__icontains=q) | 
    Q(description__icontains=q) 
    )


 headings = Heading.objects.all()
 space_count = spaces.count()
 space_messages = Communicate.objects.filter(Q(space__heading__name__icontains=q))
 
 context = {'spaces': spaces, 'headings': headings, 'space_count': space_count, 'space_messages': space_messages}
 return render(request, 'base/home.html', context)


def space(request, pk):   
 space = Space.objects.get(id=pk)
 space_messages = space.communicate_set.all() # we can query the child object of a specific space 
 participants = space.participants.all()

 if request.method == 'POST':
    message = Communicate.objects.create(
        user = request.user,
        space = space,
        body = request.POST.get('body'),
    )
    space.participants.add(request.user)
    return redirect('space', pk=space.id)

 context = {'space': space, 'space_messages': space_messages, 'participants': participants}        
 return render(request, 'base/space.html', context)



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    spaces = user.space_set.all()
    space_messages = user.communicate_set.all()
    headings = Heading.objects.all()
    context = {'user': user, 'spaces': spaces, 'space_messages': space_messages, 'headings': headings}
    return render(request, 'base/profile.html', context)


def takingPhoto(request):
    return render(request, 'takingPhoto.html')

@login_required(login_url='login')
def createSpace(request): 
    form = SpaceForm()

    if request.method == 'POST':
       form = SpaceForm(request.POST)
       if form.is_valid():
        form.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/space_form.html', context)
 
@login_required(login_url='login')
def updateSpace(request, pk):
        space = Space.objects.get(id=pk)
        form = SpaceForm(instance=space)

        if request.user != space.host:
            return HttpResponse('You are not allowed here!!!')

        if request.method == 'POST':
            form = SpaceForm(request.POST, instance=space)
            if form.is_valid():
                form.save()
                return redirect('home')

        context = {'form': form}
        return render(request, 'base/space_form.html', context)

@login_required(login_url='login')
def deleteSpace(request, pk):
    space = Space.objects.get(id=pk)

    if request.user != space.host:
            return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        space.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':space})



@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Communicate.objects.get(id=pk)

    if request.user != message.user:
            return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

