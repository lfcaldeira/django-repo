from django.urls import path

from . import views

urlpatterns = [
    #path("", views.submission_list, name="submission_list"),
    path('', views.index, name='index'),
    path('edit/<int:id>/<str:token>/', views.edit_submission, name='edit_submission'),
    path('approve/<int:id>/', views.approve_submission, name='approve_submission'),
    path('delete/<int:id>/', views.delete_submission, name='delete_submission'),
    path('recover/<int:id>/', views.recover_token, name='recover_token'),
    path('delete-my-map/<int:id>/', views.delete_with_token, name='delete_with_token'),
]
