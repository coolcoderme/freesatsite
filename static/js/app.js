const catalogCache = new Map();

function fillSelect(select, values, selected, anyLabel) {
  if (!select) return;
  const current = selected ?? select.dataset.current ?? "";
  select.innerHTML = "";
  if (anyLabel) {
    const any = document.createElement("option");
    any.value = "";
    any.textContent = anyLabel;
    select.appendChild(any);
  }
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    if (value === current) option.selected = true;
    select.appendChild(option);
  });
}

async function refreshCatalog() {
  const cfg = window.FREESAT_BUILDER;
  const exam = document.getElementById("exam");
  const section = document.getElementById("section");
  const topic = document.getElementById("topic");
  const difficulty = document.getElementById("difficulty");
  const demoOnly = document.querySelector('[name="demo_only"]');
  if (!cfg || !exam || !section) return;

  const params = new URLSearchParams({
    exam: exam.value,
    section: section.value || "",
    topic: topic ? topic.value : "",
    difficulty: difficulty ? difficulty.value : "",
    demo_only: demoOnly && demoOnly.checked ? "1" : "0",
  });
  const url = `${cfg.catalog}?${params.toString()}`;
  let data = catalogCache.get(url);
  if (!data) {
    const response = await fetch(url);
    data = await response.json();
    catalogCache.set(url, data);
  }
  const keepSection = section.value || cfg.section;
  const keepTopic = topic ? topic.value || cfg.topic : "";
  const allowAny = !document.getElementById("generate-form");
  fillSelect(section, data.sections || [], keepSection, allowAny ? "Any section" : null);
  if (topic) fillSelect(topic, data.topics || [], keepTopic, allowAny ? "Any topic" : null);
  const availability = document.getElementById("availability");
  if (availability && typeof data.available === "number") {
    const countField = document.getElementById("count");
    const wanted = countField ? Number(countField.value) : 0;
    const extra = wanted > data.available ? wanted - data.available : 0;
    availability.textContent = extra
      ? `${data.available} in the local bank · ${extra} additional if you add an API key`
      : `${data.available} in the local bank`;
  }
}

function wireCopyButtons() {
  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    button.addEventListener("click", async () => {
      const field = document.getElementById(button.dataset.copyTarget);
      if (!field) return;
      try {
        await navigator.clipboard.writeText(field.value || field.textContent || "");
        button.textContent = "Copied";
        setTimeout(() => { button.textContent = "Copy"; }, 1600);
      } catch (_err) {
        field.removeAttribute("class");
        field.select();
        document.execCommand("copy");
      }
    });
  });
}

function rememberKeyField() {
  const keyField = document.getElementById("api-key");
  const remember = document.getElementById("remember-key");
  if (keyField && window.localStorage.getItem("freesat.openaiKey")) {
    keyField.value = window.localStorage.getItem("freesat.openaiKey");
    if (remember) remember.checked = true;
  }
  const persist = () => {
    if (!keyField) return;
    if (remember && remember.checked && keyField.value) {
      window.localStorage.setItem("freesat.openaiKey", keyField.value);
    } else {
      window.localStorage.removeItem("freesat.openaiKey");
    }
  };
  if (remember) remember.addEventListener("change", persist);
  if (keyField) keyField.addEventListener("change", persist);
  return persist;
}

function wireGenerator() {
  const persistKey = rememberKeyField();
  const form = document.getElementById("generate-form");
  if (!form) return;
  const status = document.getElementById("generate-status");
  const preview = document.getElementById("generated-preview");
  const actions = document.getElementById("generated-actions");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    persistKey();
    const payload = Object.fromEntries(new FormData(form).entries());
    status.textContent = "Generating additional questions…";
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!data.ok) {
      status.textContent = data.error || "Could not generate additional questions.";
      return;
    }
    status.textContent = `Added ${data.created.length} additional question${data.created.length === 1 ? "" : "s"} to the bank.`;
    preview.hidden = false;
    preview.innerHTML = data.created.map((item, index) => `
      <article class="sheet-item">
        <p class="meta">${index + 1}. ${item.exam} · ${item.section} · ${item.topic} · ${item.difficulty}</p>
        ${item.stimulus ? `<pre class="stimulus">${item.stimulus}</pre>` : ""}
        <p class="prompt">${item.question}</p>
        <p class="key">Answer: ${item.answer}</p>
        <p>${item.explanation || ""}</p>
      </article>
    `).join("");
    if (actions) {
      const ids = data.created.map((item) => `<input type="hidden" name="question_id" value="${item.id}">`).join("");
      actions.hidden = false;
      actions.innerHTML = `
        <form method="post" action="/worksheet">${ids}<button class="btn primary" type="submit">Open these as a worksheet</button></form>
        <form method="post" action="/exam/start">${ids}<input type="hidden" name="minutes" value="20"><button class="btn ghost" type="submit">Sit these in the testing room</button></form>
      `;
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const builder = document.getElementById("builder-form") || document.getElementById("generate-form");
  if (builder && window.FREESAT_BUILDER) {
    ["exam", "section", "topic", "difficulty"].forEach((id) => {
      const node = document.getElementById(id);
      if (node) node.addEventListener("change", refreshCatalog);
    });
    const demo = document.querySelector('[name="demo_only"]');
    if (demo) demo.addEventListener("change", refreshCatalog);
    const countField = document.getElementById("count");
    if (countField) countField.addEventListener("input", refreshCatalog);
    refreshCatalog();
  }
  wireCopyButtons();
  wireGenerator();
});
