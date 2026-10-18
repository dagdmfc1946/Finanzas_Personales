const {test} = require("node:test");
const assert = require("node:assert/strict");
const {normalizeDocumentText, documentSectionMatches} = require("./static/preview/document.js");

test("busca sin mayúsculas ni tildes y normaliza espacios", () => {
  assert.equal(normalizeDocumentText("  PRÉSTAMOS\n y  DEUDAS "), "prestamos y deudas");
  assert.ok(documentSectionMatches("Primera ejecución: CONTRASEÑA segura", "contrasena"));
  assert.ok(documentSectionMatches("Crear\n un respaldo", "crear un"));
});

test("filtra versiones y contenido como texto literal", () => {
  assert.ok(documentSectionMatches("Versión [0.2.0-alpha.4]", "[0.2.0-alpha.4]"));
  assert.equal(documentSectionMatches("Crear una cuenta", ".*"), false);
  assert.equal(documentSectionMatches("Crear una cuenta", "respaldo"), false);
  assert.ok(documentSectionMatches("Cualquier sección", "   "));
});
