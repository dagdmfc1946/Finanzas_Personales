from functools import wraps
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction, IntegrityError, OperationalError
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe
from .account_forms import ProfileForm, UserCreateForm, UserAccessForm, DestructiveForm
from .models import Activity, AuditEvent
from .safety_services import DELETABLE, remove_record, reset_finances
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
                person.is_staff = form.cleaned_data["role"] == "admin"
                person.is_superuser = False
                person.save()
                Activity.objects.create(owner=person, name="Personal / trabajo principal")
                AuditEvent.objects.create(owner=request.user, action="alta de usuario", entity=str(person.pk), after={"usuario": person.username, "rol": form.cleaned_data["role"]})
            messages.success(request, "Usuario creado con finanzas vacías. Para llevar sus cuentas, cierra tu sesión y entra con ese usuario.")
            return redirect("ledger:users")
        except IntegrityError:
            form.add_error("username", "Ese nombre ya está registrado. Elige otro.")
    return render(request, "ledger/account.html", account_context("Crear usuario", form=form, notice="Las dos contraseñas nuevas son para el usuario creado. La contraseña de administrador es la tuya y autoriza el alta."), status=400 if request.method == "POST" else 200)


@admin_required
@require_http_methods(["GET", "POST"])
def user_access(request, pk):
    person = get_object_or_404(get_user_model(), pk=pk)
    form = UserAccessForm(request.POST or None, actor=request.user, initial={"role": "admin" if person.is_staff else "normal", "is_active": person.is_active})
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            person = get_user_model().objects.select_for_update().get(pk=pk)
            if person.pk == request.user.pk or person.is_superuser:
                form.add_error(None, "No puedes cambiar tu propio rol/acceso ni gestionar una cuenta superusuario desde aquí.")
            else:
                before = {"activo": person.is_active, "administrador": person.is_staff}
                person.is_staff = form.cleaned_data["role"] == "admin"
                person.is_active = form.cleaned_data["is_active"]
                person.save(update_fields=["is_staff", "is_active"])
                AuditEvent.objects.create(owner=request.user, action="acceso de usuario", entity=str(person.pk), before=before, after={"activo": person.is_active, "administrador": person.is_staff})
                messages.success(request, "Acceso actualizado. Sus finanzas se conservan.")
                return redirect("ledger:users")
    return render(request, "ledger/account.html", account_context("Acceso de " + person.username, form=form, notice="Desactivar impide entrar y conserva los registros. Esta pantalla no permite ver finanzas ni cambiar contraseñas de otros usuarios."), status=400 if request.method == "POST" else 200)


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
