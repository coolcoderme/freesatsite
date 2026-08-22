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
    availability.textContent = `${data.available} available`;
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

function wireGenerator() {
  const form = document.getElementById("generate-form");
  if (!form) return;
  const keyField = document.getElementById("api-key");
  const remember = document.getElementById("remember-key");
  const status = document.getElementById("generate-status");
  const preview = document.getElementById("generated-preview");
  if (keyField && window.localStorage.getItem("freesat.openaiKey")) {
    keyField.value = window.localStorage.getItem("freesat.openaiKey");
    if (remember) remember.checked = true;
  }
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = Object.fromEntries(new FormData(form).entries());
    if (remember && remember.checked) {
      window.localStorage.setItem("freesat.openaiKey", payload.api_key);
    } else {
      window.localStorage.removeItem("freesat.openaiKey");
    }
    status.textContent = "Creating questions…";
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!data.ok) {
      status.textContent = data.error || "Could not create questions.";
      return;
    }
    status.textContent = `Added ${data.created.length} question${data.created.length === 1 ? "" : "s"} to the bank.`;
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
    refreshCatalog();
  }
  wireCopyButtons();
  wireGenerator();
});
