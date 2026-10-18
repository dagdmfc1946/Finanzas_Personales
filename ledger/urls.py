from django.urls import path
from . import views

app_name = "ledger"
urlpatterns = [
    path("", views.section, name="home"),
    path("respaldo/descargar/", views.backup, name="backup"),
    path("catalogo/<str:kind>/nuevo/", views.catalog, name="catalog-new"),
    path("catalogo/<str:kind>/<uuid:pk>/", views.catalog, name="catalog-edit"),
    path("movimiento/nuevo/", views.entry_edit, name="entry-new"),
    path("movimiento/<uuid:pk>/", views.entry_edit, name="entry-edit"),
    path("movimiento/<uuid:pk>/anular/", views.entry_void, name="entry-void"),
    path("<slug:section>/", views.section, name="section"),
]
