const form = document.querySelector("#query-form");
const queryInput = document.querySelector("#query");
const submit = document.querySelector("#submit");
const status = document.querySelector("#status");
const result = document.querySelector("#result");

const LABELS = {
  hr: "RR. HH.",
  tech: "IT Support",
  finance: "Finance",
  out_of_scope: "Fuera de alcance",
};

document.querySelectorAll("[data-example]").forEach((button) => {
  button.addEventListener("click", () => {
    queryInput.value = button.dataset.example;
    queryInput.focus();
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = queryInput.value.trim();
  if (!query) {
    return;
  }

  submit.disabled = true;
  status.textContent = "Clasificando y buscando en la documentación…";
  result.hidden = true;

  try {
    const response = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const body = await response.json();
    if (!response.ok) {
      throw new Error(messageFrom(body));
    }
    render(body);
    status.textContent = "";
  } catch (error) {
    status.textContent = error.message || "No hay conexión con el servidor.";
  } finally {
    submit.disabled = false;
  }
});

function messageFrom(body) {
  if (typeof body.detail === "string") {
    return body.detail;
  }
  return "No se pudo completar la consulta.";
}

function render(body) {
  result.hidden = false;
  const department = document.querySelector("#department");
  department.textContent = LABELS[body.department] || body.department;
  department.dataset.department = body.department;
  document.querySelector("#confidence").textContent =
    `Confianza ${Math.round(body.confidence * 100)}%`;
  document.querySelector("#reason").textContent = body.reason;
  document.querySelector("#answer").textContent = body.answer;

  const sources = document.querySelector("#sources");
  sources.replaceChildren();
  if (!body.sources.length) {
    const item = document.createElement("li");
    const note = document.createElement("p");
    note.className = "empty";
    note.textContent = "Ningún documento. Esta respuesta no pasó por un agente RAG.";
    item.append(note);
    sources.append(item);
    return;
  }

  for (const source of body.sources) {
    const item = document.createElement("li");
    const title = document.createElement("p");
    title.className = "source-title";
    title.textContent = `${source.source} · ${Number(source.score).toFixed(2)}`;
    const excerpt = document.createElement("p");
    excerpt.className = "excerpt";
    excerpt.textContent = source.excerpt;
    item.append(title, excerpt);
    sources.append(item);
  }
}
