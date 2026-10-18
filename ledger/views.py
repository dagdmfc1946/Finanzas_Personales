from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, OperationalError, transaction
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_safe
from .forms import AccountForm, ActivityForm, CategoryForm, EntryFilter, EntryForm, VoidForm
from .models import Account, Activity, AuditEvent, Category, Entry, Installation
from .services import save_entry, summary, void_entry
from .backups import write_backup

NAVIGATION = [("resumen", "Resumen", ""), ("movimientos", "Movimientos", ""), ("sueldo", "Mi sueldo", ""), ("organizacion", "Actividades y cuentas", ""), ("historial", "Historial", ""), ("respaldo", "Respaldos", ""), ("revision", "Revisar esta fase", "")]


def context(section, title=None, **kwargs):
    return {"financial": True, "section": section, "title": title or dict((slug, label) for slug, label, _ in NAVIGATION)[section], "navigation": NAVIGATION, "version": settings.APP_VERSION, **kwargs}


@require_safe
def start(request):
    if not Installation.objects.exists():
        return redirect("setup")
    return redirect("ledger:home")


@require_http_methods(["GET", "POST"])
def setup(request):
    if Installation.objects.exists():
        return redirect("login")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save(commit=False)
                user.is_staff = True
                user.save()
                Installation.objects.create(pk=1, user=user)
                Activity.objects.create(owner=user, name="Personal / trabajo principal")
            login(request, user)
            return redirect("ledger:home")
        except (IntegrityError, OperationalError):
            form.add_error(None, "No se completó la configuración. Recarga para comprobar si ya fue creada.")
    return render(request, "ledger/access.html", {"form": form, "title": "Configurar mi usuario", "setup": True}, status=400 if request.method == "POST" else 200)


@login_required
@require_safe
def section(request, section="resumen"):
    if section not in {slug for slug, _, _ in NAVIGATION}:
        raise Http404
    form = EntryFilter(request.GET, user=request.user)
    valid = form.is_valid()
    data = form.cleaned_data if valid else {}
    selected = data.get("activity")
    entries = Entry.objects.filter(owner=request.user).select_related("activity", "account", "category", "destination_activity", "destination_account")
    if not data.get("void"):
        entries = entries.filter(void=False)
    if selected:
        entries = entries.filter(Q(activity=selected) | Q(destination_activity=selected))
    if data.get("kind"):
        entries = entries.filter(kind=data["kind"])
    if data.get("q"):
        entries = entries.filter(description__icontains=data["q"])
    if data.get("start"):
        entries = entries.filter(date__gte=data["start"])
    if data.get("end"):
        entries = entries.filter(date__lte=data["end"])
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "ledger/page.html", context(section,
        totals=summary(request.user, selected), filter=form, selected=selected,
        activities=Activity.objects.filter(owner=request.user),
        account_list=Account.objects.filter(owner=request.user), categories=Category.objects.filter(owner=request.user),
        entries=Paginator(entries, 30).get_page(request.GET.get("page")), query_params=params.urlencode(),
        events=Paginator(AuditEvent.objects.filter(owner=request.user), 30).get_page(request.GET.get("page")),
    ), status=200 if valid else 400)


@login_required
@require_http_methods(["GET", "POST"])
def catalog(request, kind, pk=None):
    types = {"actividad": (Activity, ActivityForm), "cuenta": (Account, AccountForm), "categoria": (Category, CategoryForm)}
    if kind not in types:
        raise Http404
    model, form_type = types[kind]
    instance = get_object_or_404(model, pk=pk, owner=request.user) if pk else model(owner=request.user)
    form = form_type(request.POST or None, user=request.user, instance=instance)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                before = {"name": model.objects.get(pk=pk).name} if pk else {}
                if kind == "categoria" and pk:
                    old = model.objects.get(pk=pk)
                    before.update(kind=old.kind, group=old.group)
                item = form.save(commit=False)
                item.full_clean()
                item.save()
                AuditEvent.objects.create(owner=request.user, action="catálogo", entity=str(item.pk), before=before, after={"tipo": kind, "nombre": item.name, **({"clase": item.kind, "grupo": item.group} if kind == "categoria" else {})})
                if kind == "cuenta" and not pk and form.cleaned_data.get("initial_amount"):
                    save_entry(Entry(owner=request.user, kind="inicial", cents=int(form.cleaned_data["initial_amount"] * 100),
                        activity=form.cleaned_data["initial_activity"], account=item, date=timezone.localdate(), description="Saldo inicial de " + item.name), request.user)
            messages.success(request, "Se guardaron los cambios.")
            return redirect("ledger:section", section="organizacion")
        except ValidationError as error:
            form.add_error(None, ValidationError(error.messages))
        except IntegrityError:
            form.add_error(None, "Ya existe un registro con esos datos. Revisa el nombre y el tipo.")
    return render(request, "ledger/form.html", context("organizacion", ("Editar " if pk else "Crear ") + {"actividad": "actividad", "cuenta": "cuenta", "categoria": "categoría"}[kind], form=form, category_groups=Category.objects.filter(owner=request.user).exclude(group="").order_by("group").values_list("group", flat=True).distinct()), status=400 if request.method == "POST" else 200)


@login_required
@require_http_methods(["GET", "POST"])
def entry_edit(request, pk=None):
    instance = get_object_or_404(Entry, pk=pk, owner=request.user, void=False) if pk else Entry(owner=request.user)
    form = EntryForm(request.POST or None, instance=instance, user=request.user)
    if request.method == "POST" and form.is_valid():
        try:
            save_entry(form.save(commit=False), request.user, form.cleaned_data["version"] if pk else None, form.cleaned_data.get("reason", ""))
            messages.success(request, "Movimiento guardado. Los saldos se actualizaron.")
            return redirect("ledger:section", section="movimientos")
        except ValidationError as error:
            form.add_error(None, ValidationError(error.messages))
        except IntegrityError:
            form.add_error(None, "Ese formulario ya se registró. Revisa el historial antes de intentar nuevamente.")
    return render(request, "ledger/form.html", context("movimientos", "Corregir movimiento" if pk else "Nuevo movimiento", form=form, entry_form=True), status=400 if request.method == "POST" else 200)


@login_required
@require_http_methods(["GET", "POST"])
def entry_void(request, pk):
    entry = get_object_or_404(Entry, pk=pk, owner=request.user)
    form = VoidForm(request.POST or None, initial={"version": entry.revision})
    if request.method == "POST" and form.is_valid():
        try:
            void_entry(entry, request.user, form.cleaned_data["version"], form.cleaned_data["reason"])
            messages.success(request, "Movimiento anulado; el registro y su historial se conservan.")
            return redirect("ledger:section", section="movimientos")
        except ValidationError as error:
            form.add_error(None, ValidationError(error.messages))
    return render(request, "ledger/form.html", context("movimientos", "Anular movimiento", form=form, entry=entry), status=400 if request.method == "POST" else 200)


@login_required
@require_http_methods(["POST"])
def backup(request):
    try:
        path, raw = write_backup(request.user)
    except (ValidationError, OSError, OperationalError):
        messages.error(request, "No se pudo crear el respaldo. Comprueba el espacio y los permisos de la carpeta backups.")
        return redirect("ledger:section", section="respaldo")
    response = HttpResponse(raw, content_type="application/json")
    response["Content-Disposition"] = f'attachment; filename="{path.name}"'
    return response
