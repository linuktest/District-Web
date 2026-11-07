from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.entry, name='entry'),
    path('verify/', views.verify, name='verify'),
    path('submit/', views.submit, name='submit'),
]
