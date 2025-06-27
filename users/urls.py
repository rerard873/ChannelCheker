from multiprocessing.resource_tracker import register

from django.urls import path


from users.views import login, profile,register,logout

app_name = 'users'

urlpatterns = [
    path('', profile, name = 'profile'),
    path('login/', login, name = 'login'),
    path('register/', register, name = 'register'),
    path('logout/', logout, name = 'logout'),
]