from django import forms
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_safe

from .demo import ACCOUNTS, BUDGET, NAVIGATION, TRANSACTIONS


class MovementFilter(forms.Form):
    q = forms.CharField(label="Buscar movimiento", max_length=80, required=False)
    tipo = forms.ChoiceField(
        label="Tipo de movimiento",
        choices=[("", "Todos los tipos"), ("ingreso", "Ingresos"), ("gasto", "Gastos"), ("transferencia", "Transferencias")],
        required=False,
    )


@require_safe
def page(request, section="resumen"):
    titles = {slug: title for slug, title, _ in NAVIGATION}
    if section not in titles:
        raise Http404("Sección no disponible")
    form = MovementFilter(request.GET if section == "movimientos" else {})
    valid = form.is_valid()
    movements = TRANSACTIONS
    if section == "movimientos" and valid:
        query = form.cleaned_data["q"].casefold()
        kind = form.cleaned_data["tipo"]
        movements = tuple(row for row in TRANSACTIONS if (
            (not kind or row["kind"] == kind)
            and query in " ".join((row["description"], row["category"], row["account"])).casefold()
        ))
    income = sum(row["amount"] for row in TRANSACTIONS if row["kind"] == "ingreso")
    expenses = sum(row["amount"] for row in TRANSACTIONS if row["kind"] == "gasto")
    return render(request, "preview/page.html", {
        "section": section, "title": titles[section], "navigation": NAVIGATION,
        "version": settings.APP_VERSION, "movements": movements, "filter": form,
        "accounts": ACCOUNTS, "budgets": BUDGET,
        "income": income, "expenses": expenses, "balance": income - expenses,
    }, status=200 if valid else 400)
