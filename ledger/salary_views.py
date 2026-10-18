from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods,require_safe
from django import forms
from django.urls import reverse
from .models import Salary,SalaryReceipt
from .views import context
from .salary_forms import SalaryForm,SalaryFilter,ReceiptForm
from .salary_services import save_salary,link_receipt,unlink_receipt,salary_totals


@login_required
@require_safe
def page(request):
    data=request.GET.copy()
    if "month" not in data: data["month"]=timezone.localdate().strftime("%Y-%m")
    form=SalaryFilter(data,user=request.user)
    valid=form.is_valid()
    totals=salary_totals(request.user,form.cleaned_data["month"],form.cleaned_data.get("activity")) if valid else {"rows":[],"planned":0,"received":0,"pending":0}
    return render(request,"ledger/salary.html",context("sueldo",form=form,totals=totals),status=200 if valid else 400)


@login_required
@require_http_methods(["GET","POST"])
def edit(request,pk=None):
    instance=get_object_or_404(Salary,pk=pk,owner=request.user) if pk else Salary(owner=request.user)
    form=SalaryForm(request.POST or None,user=request.user,instance=instance)
    if request.method=="POST" and form.is_valid():
        try:
            salary=save_salary(form.instance,request.user,form.cleaned_data["version"] if pk else None,form.cleaned_data.get("reason",""))
            messages.success(request,"Sueldo previsto guardado. No se crearon movimientos ni se alteraron saldos.")
            return redirect(reverse("ledger:salary")+"?month="+salary.budget_month.strftime("%Y-%m"))
        except ValidationError as error: form.add_error(None,ValidationError(error.messages))
        except IntegrityError: form.add_error(None,"Este formulario ya fue registrado. Revisa Mi sueldo antes de reenviarlo.")
    return render(request,"ledger/form.html",context("sueldo","Corregir sueldo" if pk else "Nuevo sueldo previsto",form=form),status=400 if request.method=="POST" else 200)


@login_required
@require_http_methods(["GET","POST"])
def receipt(request,pk):
    salary=get_object_or_404(Salary,pk=pk,owner=request.user)
    form=ReceiptForm(request.POST or None,user=request.user,salary=salary)
    if request.method=="POST" and form.is_valid():
        try:
            link_receipt(salary,form.cleaned_data["entry"],request.user)
            messages.success(request,"Cobro vinculado al ingreso existente, sin duplicarlo.")
            return redirect(reverse("ledger:salary")+"?month="+salary.budget_month.strftime("%Y-%m"))
        except (ValidationError,IntegrityError): form.add_error(None,"No se vinculó: revisa que sea un ingreso propio vigente, de esta actividad y sin vínculo previo.")
    return render(request,"ledger/form.html",context("sueldo","Vincular cobro: "+salary.title,form=form),status=400 if request.method=="POST" else 200)


class UnlinkForm(forms.Form):
    reason=forms.CharField(label="Motivo de desvinculación",max_length=240)
    confirm=forms.BooleanField(label="Confirmo desvincular el cobro; el ingreso seguirá registrado")


@login_required
@require_http_methods(["GET","POST"])
def unlink(request,pk):
    receipt=get_object_or_404(SalaryReceipt,pk=pk,owner=request.user)
    form=UnlinkForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        salary=receipt.salary
        unlink_receipt(receipt,request.user,form.cleaned_data["reason"])
        messages.success(request,"Cobro desvinculado; el ingreso y su saldo se conservan.")
        return redirect(reverse("ledger:salary")+"?month="+salary.budget_month.strftime("%Y-%m"))
    return render(request,"ledger/form.html",context("sueldo","Desvincular cobro",form=form),status=400 if request.method=="POST" else 200)
