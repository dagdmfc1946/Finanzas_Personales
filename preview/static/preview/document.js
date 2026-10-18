"use strict";

function normalizeDocumentText(value) {
  return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("es").replace(/\s+/g, " ").trim();
}

function documentSectionMatches(text, query) {
  return normalizeDocumentText(text).includes(normalizeDocumentText(query));
}

function initDocumentReader() {
  const article = document.querySelector(".document-content");
  const toc = document.querySelector('[aria-label="Índice del documento"]');
  const tools = document.querySelector(".document-tools");
  if (!article || !toc || !tools) return;
  const headings = Array.from(article.children).filter(node => node.tagName === "H2");
  if (!headings.length) return;

  const sections = headings.map((heading, index) => {
    const section = document.createElement("details");
    section.className = "document-section";
    section.open = index === 0;
    const summary = document.createElement("summary");
    const body = document.createElement("div");
    body.className = "document-section-body";
    article.insertBefore(section, heading);
    let sibling = heading.nextElementSibling;
    summary.append(heading);
    while (sibling && !sibling.matches("h1,h2")) {
      const next = sibling.nextElementSibling;
      body.append(sibling);
      sibling = next;
    }
    section.append(summary, body);
    return {node: section, text: [heading.textContent, ...Array.from(body.children, node => node.textContent)].join(" ")};
  });

  const indexEntries = Array.from(toc.querySelectorAll('a[href^="#"]')).map(anchor => ({
    item: anchor.closest("li"),
    target: document.getElementById(anchor.getAttribute("href").slice(1)),
  }));
  for (const item of Array.from(toc.querySelectorAll("li"))) {
    if (item.parentElement === toc.firstElementChild) continue;
    const anchor = Array.from(item.children).find(node => node.tagName === "A");
    const children = Array.from(item.children).find(node => node.tagName === "UL");
    if (!anchor || !children) continue;
    const disclosure = document.createElement("details");
    const summary = document.createElement("summary");
    summary.textContent = anchor.textContent;
    anchor.setAttribute("aria-label", "Ver " + anchor.textContent);
    anchor.textContent = "Ver esta sección";
    const jump = document.createElement("li");
    jump.className = "section-jump";
    jump.append(anchor);
    children.prepend(jump);
    disclosure.append(summary, children);
    item.replaceChildren(disclosure);
  }

  const search = document.getElementById("document-filter");
  const status = document.getElementById("document-results");
  const indexGroups = Array.from(toc.querySelectorAll("details"));
  let savedOpen = null;

  function applyFilter() {
    const query = search.value.slice(0, 120);
    const filtering = Boolean(normalizeDocumentText(query));
    if (filtering && !savedOpen) savedOpen = new Map([...sections.map(item => item.node), ...indexGroups].map(node => [node, node.open]));
    let count = 0;
    for (const section of sections) {
      const match = documentSectionMatches(section.text, query);
      section.node.hidden = !match;
      if (match) count++;
      if (filtering && match) section.node.open = true;
    }
    for (const entry of indexEntries) {
      const section = entry.target?.closest(".document-section");
      entry.item.hidden = Boolean(section?.hidden);
    }
    if (filtering) indexGroups.forEach(node => { node.open = true; });
    else if (savedOpen) {
      savedOpen.forEach((open, node) => { node.open = open; });
      savedOpen = null;
    }
    status.textContent = count ? `${count} de ${sections.length} secciones. Filtro por títulos y contenido; sin distinguir mayúsculas ni tildes.` : "No hay secciones que coincidan. Prueba otra palabra o limpia el filtro.";
  }

  search.addEventListener("input", applyFilter);
  document.getElementById("document-clear").addEventListener("click", () => {
    search.value = "";
    applyFilter();
    search.focus();
  });
  for (const [id, open] of [["document-expand", true], ["document-collapse", false]]) {
    document.getElementById(id).addEventListener("click", () => {
      sections.filter(item => !item.node.hidden).forEach(item => { item.node.open = open; });
      indexGroups.forEach(node => { node.open = open; });
    });
  }

  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target || !article.contains(target)) return;
    const section = target.closest(".document-section");
    if (section?.hidden) { search.value = ""; applyFilter(); }
    if (section) section.open = true;
    const link = Array.from(toc.querySelectorAll("a")).find(node => node.getAttribute("href") === "#" + id);
    let parent = link?.parentElement;
    while (parent && parent !== toc) {
      if (parent.tagName === "DETAILS") parent.open = true;
      parent = parent.parentElement;
    }
    target.scrollIntoView({block: "start"});
  }
  window.addEventListener("hashchange", revealHash);
  document.addEventListener("click", event => {
    if (event.target.closest('a[href^="#"]')) requestAnimationFrame(revealHash);
  });
  applyFilter();
  tools.hidden = false;
  revealHash();
}

if (typeof module !== "undefined") module.exports = {normalizeDocumentText, documentSectionMatches};
if (typeof document !== "undefined") initDocumentReader();
