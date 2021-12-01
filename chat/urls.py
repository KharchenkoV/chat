from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('account/login/', views.UserLoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('account/register/', views.RegisterPage.as_view(), name='register'),
    path('createroom/', views.createroom, name='createroom'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('<str:room>/update_room', views.updateRoom, name='update_room'),
    path('<str:room>/delete_user_from_room/<str:user>', views.deleteUserFromRoom, name='delete_user'),
    path('<str:room>/delete_room', views.deleteRoom, name='delete_room'),
    path('<str:room>/add_users', views.addUserToRoom, name='add_users'),
    path('<str:room>/add', views.addUser, name='add'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('<str:user>/display/', views.userDisplay, name='user_display'),
    path('<str:user>/edit', views.updateUser, name='user_edit'),
    path('<str:user>/delete', views.deleteUser, name='user_delete'),
]