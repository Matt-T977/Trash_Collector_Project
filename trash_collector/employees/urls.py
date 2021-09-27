from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('create.html/', views.create, name="create"),
    path('edit_profile.html/', views.edit_profile, name="edit_profile")
]
