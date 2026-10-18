"use strict";
(() => {
  const kind = document.getElementById("id_kind");
  const category = document.getElementById("id_category");
  const help = document.getElementById("entry-kind-help");
  if (!kind || !category || !help) return;
  const messages = {
    ingreso: "Ingreso: dinero que recibes ahora. Categoría opcional de Ingreso; destinos desactivados.",
    gasto: "Gasto: dinero que pagas. Categoría opcional de Gasto; destinos desactivados.",
    inicial: "Saldo inicial: dinero que ya tenías. Se registra sin categoría y sin destinos. No cuenta como ingreso nuevo.",
    transferencia: "Transferencia: mueve dinero propio. Selecciona cuenta y actividad de destino; se registra sin categoría y no crea ingresos ni gastos."
  };
  function update() {
    const categorized = ["ingreso", "gasto"].includes(kind.value);
    category.disabled = !categorized;
    for (const option of category.options) {
      option.hidden = Boolean(option.value) && option.dataset.kind !== kind.value;
      option.disabled = option.hidden;
      if (option.selected && option.disabled) category.value = "";
    }
    if (!categorized) category.value = "";
    for (const name of ["destination_activity", "destination_account"]) {
      const field = document.getElementById("id_" + name);
      field.disabled = kind.value !== "transferencia";
      field.required = !field.disabled;
      if (field.disabled) field.value = "";
    }
    help.textContent = messages[kind.value] || "Elige primero el tipo de movimiento para ver los campos que corresponden.";
  }
  kind.addEventListener("change", update);
  update();
})();
