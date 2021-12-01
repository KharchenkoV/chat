from django.core.checks import messages
from django.shortcuts import render, redirect
from chat.models import *
from .forms import RoomForm, SignUpForm
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView
import logging
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    rooms = Room.objects.filter(users__username__contains=request.user.username)
    return render(request, 'home.html',{
        'rooms' : rooms,
    })

def createroom(request):
    users = User.objects.all()
    count = len(users)
    return render(request, 'room/createroom.html',{
        'users' : users,
        'count' : count,
    })

@login_required
def room(request, room):
    username = request.GET.get('user')
    user = User.objects.get(username=username)
    room_details = Room.objects.get(name=room)
    count = room_details.users.all().count()
    users = room_details.users.all
    return render(request, 'room.html',{
        'user' : user,
        'room' : room,
        'room_details' : room_details,
        'count': count,
        'users': users,
    })

@login_required
def checkview(request):
    room = request.POST['room_name']
    user = request.POST['user']
    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?user='+user)
    else:
        users = request.POST.getlist('users[]')
        new_room = Room.objects.create(name=room)
        new_room.save()
        temp_users = []
        for i in users:
            temp_user = User.objects.get(username=i)
            temp_users.append(temp_user)
        new_room.users.set(temp_users)
        return redirect('/' + room + '/?user='+user)

def updateRoom(request, room):
    temp_room = Room.objects.get(name=room)
    form = RoomForm(instance=temp_room)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=temp_room)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form' : form}
    return render(request, 'room/redactroom.html', context)

def deleteUserFromRoom(request, room, user):
    room = Room.objects.get(name=room)
    user = User.objects.get(username=user)
    room.users.remove(user)
    return redirect('/') 

def addUserToRoom(request, room):
    room = Room.objects.get(name=room)
    logging.warning(room.users.all())
    users = User.objects.exclude(id__in=room.users.all())
    return render(request, 'room/addusers.html',{
        'users' : users,
        'room' : room.name,
    })

def addUser(request, room):
    room = Room.objects.get(name=room)
    users = request.POST.getlist('users[]')
    for i in users:
        user = User.objects.get(username=i)
        room.users.add(user.id)
    return redirect('/')

def deleteRoom(request, room):
    room = Room.objects.get(name=room)
    room.delete()
    return redirect('/')

def send(request):
    message = request.POST['message']
    usert = User.objects.get(username=request.POST['user'])
    roomt = Room.objects.get(id=request.POST['room_id']) 

    new_message = Message.objects.create(value=message, user=usert, room=roomt)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    
    return JsonResponse({"messages":list(messages.values('value', 'date', 'user__username'))})

class UserLoginView(LoginView):
    template_name = 'user/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class RegisterPage(FormView):
    template_name = 'user/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form) 


def userDisplay(request, user):
    return render(request, 'user/display.html')


def updateUser(request, user):
    user = User.objects.get(username=user)
    form = SignUpForm(instance=user)
    
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form' : form}
    return render(request, 'room/redactroom.html', context)


def deleteUser(request, user):    
    try:
        u = User.objects.get(username = user)
        u.delete()
        messages.success(request, "The user is deleted")            

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return redirect('/')

    except Exception as e: 
        return redirect('/')

    return redirect('/') 