from django.contrib.auth import views as auth
from django.urls import include, path
from ledger import views
from preview import views as demo
from preview.documents import document

urlpatterns = [
    path("", views.start, name="home"),
    path("configurar/", views.setup, name="setup"),
    path("acceso/", auth.LoginView.as_view(template_name="ledger/access.html", extra_context={"title": "Iniciar sesión"}), name="login"),
    path("salir/", auth.LogoutView.as_view(), name="logout"),
    path("clave/", auth.PasswordChangeView.as_view(template_name="ledger/access.html", success_url="/app/", extra_context={"title": "Cambiar contraseña"}), name="password-change"),
    path("app/", include("ledger.urls")),
    path("demo/", demo.page, name="demo"),
    path("documentacion/<slug:document>/", document, name="document"),
    path("<slug:section>/", demo.page, name="section"),
]
