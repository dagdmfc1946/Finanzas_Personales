from functools import wraps
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction, IntegrityError, OperationalError
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe
from .account_forms import ProfileForm, UserCreateForm, UserAccessForm, DestructiveForm, RegistrationForm
from .models import Activity, AuditEvent, Installation
from .safety_services import DELETABLE, remove_record, reset_finances, remove_user
from .views import context


def admin_required(view):
    @wraps(view)
    def checked(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return login_required(checked)


def account_context(title, **kwargs):
    return context("perfil", title, **kwargs)


@login_required
@require_safe
def profile(request):
    return render(request, "ledger/account.html", account_context("Mi perfil", mode="profile"))


@login_required
@require_http_methods(["GET", "POST"])
def profile_edit(request):
    form = ProfileForm(request.POST or None, actor=request.user)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
            messages.success(request, "Perfil actualizado. Si cambiaste tu nombre de acceso, úsalo al iniciar sesión de nuevo.")
            return redirect("ledger:profile")
        except IntegrityError:
            form.add_error("username", "Ese nombre ya está registrado. Elige otro.")
    return render(request, "ledger/account.html", account_context("Editar mi perfil", form=form), status=400 if request.method == "POST" else 200)


@login_required
@require_http_methods(["GET", "POST"])
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Contraseña actualizada. Conservas esta sesión; las otras sesiones deberán volver a entrar.")
        return redirect("ledger:profile")
    return render(request, "ledger/account.html", account_context("Cambiar contraseña", form=form), status=400 if request.method == "POST" else 200)


@admin_required
@require_safe
def users(request):
    return render(request, "ledger/account.html", account_context("Administrar usuarios", mode="users", people=get_user_model().objects.order_by("username")))


@admin_required
@require_http_methods(["GET", "POST"])
def user_create(request):
    form = UserCreateForm(request.POST or None, actor=request.user)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                person = form.save(commit=False)
                person.is_staff = False
                person.is_superuser = False
                person.save()
                Activity.objects.create(owner=person, name="Personal / trabajo principal")
                AuditEvent.objects.create(owner=request.user, action="alta de usuario", entity=str(person.pk), after={"usuario": person.username, "rol": "normal"})
            messages.success(request, "Usuario creado con finanzas vacías. Para llevar sus cuentas, cierra tu sesión y entra con ese usuario.")
            return redirect("ledger:users")
        except IntegrityError:
            form.add_error("username", "Ese nombre ya está registrado. Elige otro.")
    return render(request, "ledger/account.html", account_context("Crear usuario", form=form, notice="Las dos contraseñas nuevas son para el usuario creado. La contraseña de administrador es la tuya y autoriza el alta. Siempre se crea un usuario normal."), status=400 if request.method == "POST" else 200)


@require_http_methods(["GET", "POST"])
def register(request):
    if not Installation.objects.exists():
        return redirect("setup")
    if request.user.is_authenticated:
        return redirect("ledger:profile")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                person = form.save(commit=False)
                person.is_staff = False
                person.is_superuser = False
                person.save()
                Activity.objects.create(owner=person, name="Personal / trabajo principal")
                AuditEvent.objects.create(owner=person, action="registro de usuario", after={"rol": "normal"})
            login(request, person)
            return redirect("ledger:home")
        except IntegrityError:
            form.add_error("username", "Ese nombre ya está registrado. Elige otro.")
    return render(request, "ledger/access.html", {"form": form, "title": "Crear usuario", "registration": True}, status=400 if request.method == "POST" else 200)


@admin_required
@require_http_methods(["GET", "POST"])
def user_access(request, pk):
    person = get_object_or_404(get_user_model(), pk=pk)
    before = {"usuario": person.username, "nombres": person.first_name, "apellidos": person.last_name, "activo": person.is_active}
    form = UserAccessForm(request.POST or None, actor=request.user, instance=person)
    if request.method == "POST" and form.is_valid():
        if person.is_superuser or (Installation.objects.filter(user_id=pk).exists() and not form.cleaned_data["is_active"]):
            form.add_error(None, "El administrador inicial no puede desactivarse; las cuentas superusuario no se editan desde aquí.")
        else:
            try:
                with transaction.atomic():
                    form.save()
                    AuditEvent.objects.create(owner=request.user, action="editar usuario", entity=str(pk), before=before, after={"usuario": person.username, "nombres": person.first_name, "apellidos": person.last_name, "activo": person.is_active})
                messages.success(request, "Usuario actualizado. Su rol y sus finanzas se conservan.")
                return redirect("ledger:users")
            except IntegrityError:
                form.add_error("username", "Ese nombre ya está registrado. Elige otro.")
    return render(request, "ledger/account.html", account_context("Editar usuario: " + before["usuario"], form=form, notice="Edita nombre de acceso, nombres, apellidos y estado. Los usuarios nuevos siempre son normales; el administrador solo se crea la primera vez. Esta pantalla no muestra finanzas ni cambia contraseñas ajenas."), status=400 if request.method == "POST" else 200)


@admin_required
@require_http_methods(["GET", "POST"])
def user_delete(request, pk):
    person = get_object_or_404(get_user_model(), pk=pk)
    form = DestructiveForm(request.POST or None, actor=request.user, phrase="ELIMINAR USUARIO " + person.username)
    form.fields["current_password"].label = "Tu contraseña de administrador"
    form.fields["confirm"].label = "Confirmo eliminar el acceso y los datos del usuario seleccionado"
    if request.method == "POST" and form.is_valid():
        try:
            path = remove_user(request.user, pk, form.cleaned_data["reason"])
            messages.success(request, f"Usuario eliminado. Copia financiera previa: {path.relative_to(path.parent.parent)}. Para recuperarla debes crear un usuario y restaurar esa copia; no incluye la contraseña.")
            return redirect("ledger:users")
        except (ValidationError, OSError, OperationalError) as error:
            form.add_error(None, ValidationError(error.messages) if isinstance(error, ValidationError) else "No se completó la eliminación. Revisa el respaldo; los datos se conservan.")
    return render(request, "ledger/account.html", account_context("Eliminar usuario: " + person.username, form=form, record=person, destructive=True, notice="Se eliminará el acceso de esta persona y TODOS sus datos financieros e historial. No afecta a los demás usuarios. El administrador inicial no puede eliminarse.", backup_notice="Se crea primero una copia financiera del usuario seleccionado, sin contraseña ni perfil. Si falla, no se elimina nada. Para recuperar necesitarás recrear su usuario con una nueva clave y restaurar la copia, como explica el manual."), status=400 if request.method == "POST" else 200)


@login_required
@require_http_methods(["GET", "POST"])
def delete(request, kind, pk):
    if kind not in DELETABLE:
        raise Http404
    item = get_object_or_404(DELETABLE[kind], pk=pk, owner=request.user)
    form = DestructiveForm(request.POST or None, actor=request.user, phrase="ELIMINAR", initial={"version": getattr(item, "revision", 0)})
    if request.method == "POST" and form.is_valid():
        try:
            path = remove_record(request.user, kind, item.pk, form.cleaned_data["version"], form.cleaned_data["reason"])
            messages.success(request, f"Registro eliminado. Copia recuperable previa: {path.relative_to(path.parent.parent)}.")
            if kind == "sueldo":
                return redirect(reverse("ledger:salary") + "?month=" + item.budget_month.strftime("%Y-%m"))
            return redirect("ledger:section", section="movimientos" if kind == "movimiento" else "organizacion")
        except (ValidationError, OSError, OperationalError) as error:
            form.add_error(None, ValidationError(error.messages) if isinstance(error, ValidationError) else "No se pudo completar la operación. Revisa espacio/permisos; no se eliminaron datos.")
    notice = {"movimiento": "Se retirará el movimiento y sus vínculos de cobro; cambiará el saldo calculado. El plan de sueldo se conserva.", "sueldo": "Se eliminarán el plan y sus vínculos; los ingresos y saldos reales se conservan."}.get(kind, "Solo se elimina si no está en uso. Si tiene movimientos o planes, corrige o elimina primero esas referencias.")
    return render(request, "ledger/account.html", account_context("Eliminar " + kind, form=form, notice=notice, record=item, destructive=True), status=400 if request.method == "POST" else 200)


@login_required
@require_http_methods(["GET", "POST"])
def reset(request):
    form = DestructiveForm(request.POST or None, actor=request.user, phrase="REINICIAR " + request.user.username)
    if request.method == "POST" and form.is_valid():
        try:
            path = reset_finances(request.user, form.cleaned_data["reason"])
            messages.success(request, f"Tus finanzas empiezan de cero. Tu acceso y los demás usuarios se conservaron. Copia previa: {path.relative_to(path.parent.parent)}.")
            return redirect("ledger:home")
        except (ValidationError, OSError, OperationalError) as error:
            form.add_error(None, ValidationError(error.messages) if isinstance(error, ValidationError) else "No se pudo completar el reinicio. Revisa espacio/permisos; no se eliminaron datos.")
    return render(request, "ledger/account.html", account_context("Reiniciar mis datos", form=form, destructive=True, notice="Borra SOLO tus movimientos, cuentas, categorías, sueldos, vínculos e historial. Crea una actividad personal vacía y un evento de reinicio. Conserva tu usuario, contraseña, perfil, rol, copias y TODOS los datos de otras personas. No borra el archivo de la base de datos."), status=400 if request.method == "POST" else 200)
