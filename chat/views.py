from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def room(request, room):
    username = request.GET.get('user')
    user = User.objects.get(username=username)
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html',{
        'user' : user,
        'room' : room,
        'room_details' : room_details,
    })

@login_required
def checkview(request):
    room = request.POST['room_name']
    user = request.POST['user']

    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?user='+user)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?user='+user)

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
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form) 