(() => {
  const root = document.getElementById("exam-app");
  if (!root || !window.FREESAT_EXAM) return;

  const questions = window.FREESAT_EXAM;
  const examId = root.dataset.examId;
  const saveUrl = root.dataset.saveUrl;
  const minutes = Number(root.dataset.minutes || 20);
  const storageKey = `freesat.exam.${examId}`;

  const state = loadState() || {
    index: 0,
    answers: {},
    flags: [],
    notes: {},
    eliminated: {},
    remaining: minutes * 60,
    highlightOn: false,
  };

  const rail = document.getElementById("exam-rail");
  const meta = document.getElementById("exam-meta");
  const passage = document.getElementById("exam-passage");
  const prompt = document.getElementById("exam-prompt");
  const answers = document.getElementById("exam-answers");
  const flag = document.getElementById("mark-review");
  const timer = document.getElementById("exam-timer");
  const review = document.getElementById("exam-review");
  const reviewList = document.getElementById("review-list");
  const noteBox = document.getElementById("note-box");
  const calcDisplay = document.getElementById("calc-display");

  function loadState() {
    try {
      return JSON.parse(localStorage.getItem(storageKey) || "null");
    } catch (_err) {
      return null;
    }
  }

  function persist() {
    localStorage.setItem(storageKey, JSON.stringify(state));
    fetch(saveUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers: state.answers, flags: state.flags }),
    }).catch(() => {});
  }

  function current() {
    return questions[state.index];
  }

  function renderRail() {
    rail.innerHTML = "";
    questions.forEach((item, index) => {
      const button = document.createElement("button");
      button.className = "rail-btn";
      button.textContent = String(index + 1);
      if (index === state.index) button.classList.add("current");
      if (state.answers[item.id]) button.classList.add("answered");
      if (state.flags.includes(item.id)) button.classList.add("flagged");
      button.addEventListener("click", () => {
        state.index = index;
        draw();
      });
      rail.appendChild(button);
    });
  }

  function renderChoices(item) {
    answers.innerHTML = "";
    if (item.type === "grid_in") {
      const input = document.createElement("input");
      input.type = "text";
      input.value = state.answers[item.id] || "";
      input.placeholder = "Enter a number";
      input.addEventListener("input", () => {
        state.answers[item.id] = input.value;
        persist();
        renderRail();
      });
      answers.appendChild(input);
      return;
    }
    const eliminated = new Set(state.eliminated[item.id] || []);
    Object.entries(item.choices || {}).forEach(([letter, text]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "choice";
      if (state.answers[item.id] === letter) button.classList.add("selected");
      if (eliminated.has(letter)) button.classList.add("eliminated");
      button.innerHTML = `<b>${letter}</b><span>${text}</span>`;
      button.addEventListener("click", (event) => {
        if (event.altKey || event.shiftKey) {
          const next = new Set(state.eliminated[item.id] || []);
          if (next.has(letter)) next.delete(letter);
          else next.add(letter);
          state.eliminated[item.id] = [...next];
        } else {
          state.answers[item.id] = letter;
        }
        persist();
        draw();
      });
      answers.appendChild(button);
    });
  }

  function draw() {
    const item = current();
    if (!item) return;
    review.hidden = true;
    document.getElementById("exam-stage").hidden = false;
    meta.textContent = `Question ${state.index + 1} of ${questions.length}  ·  ${item.exam}  ·  ${item.section}  ·  ${item.topic}  ·  ${item.difficulty}`;
    passage.textContent = item.stimulus || "";
    prompt.textContent = item.question;
    flag.checked = state.flags.includes(item.id);
    if (noteBox) noteBox.value = state.notes[item.id] || "";
    renderChoices(item);
    renderRail();
  }

  function formatTime(total) {
    const safe = Math.max(0, total);
    const mins = String(Math.floor(safe / 60)).padStart(2, "0");
    const secs = String(safe % 60).padStart(2, "0");
    return `${mins}:${secs}`;
  }

  function tick() {
    state.remaining -= 1;
    timer.textContent = formatTime(state.remaining);
    timer.classList.toggle("warn", state.remaining <= 300);
    timer.classList.toggle("hot", state.remaining <= 60);
    if (state.remaining <= 0) {
      document.getElementById("submit-form").requestSubmit();
      return;
    }
    persist();
  }

  function showReview() {
    document.getElementById("exam-stage").hidden = true;
    review.hidden = false;
    const unanswered = questions.filter((q) => !state.answers[q.id]);
    const flagged = questions.filter((q) => state.flags.includes(q.id));
    const chips = [
      ...unanswered.map((q) => ({ q, label: `Unanswered ${questions.indexOf(q) + 1}` })),
      ...flagged.map((q) => ({ q, label: `Flagged ${questions.indexOf(q) + 1}` })),
      ...questions.map((q) => ({ q, label: String(questions.indexOf(q) + 1) })),
    ];
    reviewList.innerHTML = "";
    chips.forEach(({ q, label }) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "review-chip";
      button.textContent = label;
      button.addEventListener("click", () => {
        state.index = questions.findIndex((item) => item.id === q.id);
        draw();
      });
      reviewList.appendChild(button);
    });
  }

  document.getElementById("prev-q").addEventListener("click", () => {
    state.index = Math.max(0, state.index - 1);
    draw();
  });
  document.getElementById("next-q").addEventListener("click", () => {
    state.index = Math.min(questions.length - 1, state.index + 1);
    draw();
  });
  document.getElementById("review-btn").addEventListener("click", showReview);
  flag.addEventListener("change", () => {
    const id = current().id;
    state.flags = state.flags.filter((item) => item !== id);
    if (flag.checked) state.flags.push(id);
    persist();
    renderRail();
  });

  document.querySelectorAll("[data-tool]").forEach((button) => {
    button.addEventListener("click", () => {
      const tool = button.dataset.tool;
      if (tool === "highlight") {
        state.highlightOn = !state.highlightOn;
        button.classList.toggle("active", state.highlightOn);
        return;
      }
      const modal = {
        notes: "notes-modal",
        calc: "calc-modal",
        ref: "ref-modal",
      }[tool];
      if (modal) document.getElementById(modal).hidden = false;
    });
  });
  document.querySelectorAll("[data-close]").forEach((button) => {
    button.addEventListener("click", () => {
      document.getElementById(button.dataset.close).hidden = true;
    });
  });
  if (noteBox) {
    noteBox.addEventListener("input", () => {
      state.notes[current().id] = noteBox.value;
      persist();
    });
  }
  passage.addEventListener("mouseup", () => {
    if (!state.highlightOn) return;
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) return;
    const range = selection.getRangeAt(0);
    const mark = document.createElement("mark");
    mark.className = "hl";
    range.surroundContents(mark);
    selection.removeAllRanges();
  });

  const keys = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "C", "+", "="];
  const grid = document.getElementById("calc-grid");
  let expr = "";
  keys.forEach((key) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = key;
    button.addEventListener("click", () => {
      if (key === "C") expr = "";
      else if (key === "=") {
        if (!/^[0-9.+\-*/() ]+$/.test(expr)) {
          expr = "Error";
        } else {
          try {
            expr = String(Function(`"use strict"; return (${expr})`)());
          } catch (_err) {
            expr = "Error";
          }
        }
      } else {
        expr += key;
      }
      calcDisplay.value = expr || "0";
    });
    grid.appendChild(button);
  });

  document.getElementById("submit-form").addEventListener("submit", () => {
    document.getElementById("submit-answers").value = JSON.stringify(state.answers);
    localStorage.removeItem(storageKey);
  });

  timer.textContent = formatTime(state.remaining);
  draw();
  setInterval(tick, 1000);
})();
