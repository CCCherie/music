from django.urls import path
from . import views

urlpatterns=[
    path('login.html',views.loginView,name='login'),
    path('home/<int:page>.html',views.homeView,name='home'),
    path('logout.html',views.logoutView,name='logout'),
]
