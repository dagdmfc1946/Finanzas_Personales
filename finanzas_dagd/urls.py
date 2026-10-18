from django.urls import path
from preview import views

urlpatterns = [
    path("", views.page, name="home"),
    path("<slug:section>/", views.page, name="section"),
]
