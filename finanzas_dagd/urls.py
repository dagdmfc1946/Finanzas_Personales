from django.contrib.auth import views as auth
from django.urls import include, path
from ledger import views, account_views
from preview import views as demo
from preview.documents import document

urlpatterns = [
    path("", views.start, name="home"),
    path("configurar/", views.setup, name="setup"),
    path("registro/", account_views.register, name="register"),
    path("acceso/", auth.LoginView.as_view(template_name="ledger/access.html", extra_context={"title": "Iniciar sesión"}), name="login"),
    path("salir/", auth.LogoutView.as_view(), name="logout"),
    path("clave/", account_views.password_change, name="password-change"),
    path("app/", include("ledger.urls")),
    path("demo/", demo.page, name="demo"),
    path("documentacion/<slug:document>/", document, name="document"),
    path("<slug:section>/", demo.page, name="section"),
]
