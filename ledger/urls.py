from django.urls import path
from . import views, salary_views

app_name = "ledger"
urlpatterns = [
    path("", views.section, name="home"),
    path("sueldo/", salary_views.page, name="salary"),
    path("sueldo/nuevo/", salary_views.edit, name="salary-new"),
    path("sueldo/<uuid:pk>/", salary_views.edit, name="salary-edit"),
    path("sueldo/<uuid:pk>/cobro/", salary_views.receipt, name="salary-receipt"),
    path("sueldo/cobro/<uuid:pk>/desvincular/", salary_views.unlink, name="salary-unlink"),
    path("respaldo/descargar/", views.backup, name="backup"),
    path("catalogo/<str:kind>/nuevo/", views.catalog, name="catalog-new"),
    path("catalogo/<str:kind>/<uuid:pk>/", views.catalog, name="catalog-edit"),
    path("movimiento/nuevo/", views.entry_edit, name="entry-new"),
    path("movimiento/<uuid:pk>/", views.entry_edit, name="entry-edit"),
    path("movimiento/<uuid:pk>/anular/", views.entry_void, name="entry-void"),
    path("<slug:section>/", views.section, name="section"),
]
