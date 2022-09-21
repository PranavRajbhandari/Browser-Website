from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required   
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm  # it has three fields:username,password1 and password 2
from .models import Room, Topic #now importing data where we saved in admin database
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name':'lets learn python'},
#     {'id': 2, 'name':'Design with me'},
#     {'id': 3, 'name':'Frontend developers'},
# ]

def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)#it will give error or return back user object

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request,'Username or Password does not exist')


    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='register'
    form = UserCreationForm()

    if request.method =='POST':
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''  #Search button

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | #this means or statement
        Q(name__icontains=q)|          #this room is create for search button 
        Q(description__icontains=q)
    ) #.models sameasabove

    topics = Topic.objects.all()
    room_count =rooms.count() #rembember 's' 

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context )

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'base/room.html',context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    #now only host or specific account users can update

    if request.user != room.host: #!=not equal
        return HttpResponse('you are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render (request, 'base/room_form.html', context)


    
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk) 

    if request.user != room.host: #!=not equal
        return HttpResponse('you are not allowed here!!')

    if request.method == 'POST':
            room.delete()
            return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

