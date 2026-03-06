from django.urls import path

from . import views

urlpatterns = [
    #path("", views.submission_list, name="submission_list"),
    path('', views.index, name='index'),
]
