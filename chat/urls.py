from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('account/login/', views.UserLoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('account/register/', views.RegisterPage.as_view(), name='register'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]