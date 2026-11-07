from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('leadership/', views.leadership, name='leadership'),
    path('clubs/', views.clubs, name='clubs'),
    path('calendar/', views.district_calendar, name='calendar'),
]
