const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
if (tg) {
  tg.ready();
  tg.expand();
}

const view = document.getElementById("view");
const titleEl = document.getElementById("title");
const backButton = document.getElementById("back");
const searchButton = document.getElementById("search-button");
const modeBar = document.getElementById("mode");
const loader = document.getElementById("loader");
const loaderFill = document.getElementById("loader-fill");

let loaderTimer = null;
let loaderProgress = 0;

function startLoader() {
  if (!loader) return;
  loaderProgress = 0;
  loader.classList.remove("hidden");
  loaderFill.style.width = "0%";
  loaderTimer = setInterval(() => {
    loaderProgress = Math.min(loaderProgress + 6 + Math.random() * 9, 90);
    loaderFill.style.width = loaderProgress + "%";
  }, 160);
}

function finishLoader() {
  if (!loader) return;
  if (loaderTimer) {
    clearInterval(loaderTimer);
    loaderTimer = null;
  }
  loaderFill.style.width = "100%";
  setTimeout(() => loader.classList.add("hidden"), 250);
}

const nav = { stack: [] };
const topicCache = new Map();
let treePromise = null;
let mode = "konspekt";
let currentTopic = null;

function setModeVisible(visible) {
  if (modeBar) modeBar.hidden = !visible;
}

function updateModeButtons() {
  if (!modeBar) return;
  modeBar.querySelectorAll("button").forEach((button) => {
    button.classList.toggle("active", button.dataset.mode === mode);
  });
}

if (modeBar) {
  modeBar.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      mode = button.dataset.mode;
      updateModeButtons();
      if (currentTopic) renderTopic(currentTopic);
    });
  });
}

function haptic() {
  if (tg && tg.HapticFeedback) tg.HapticFeedback.impactOccurred("light");
}

function setTitle(text) {
  titleEl.textContent = text;
  document.title = text;
}

function clearView() {
  view.innerHTML = "";
}

function renderMessage(text) {
  setModeVisible(false);
  currentTopic = null;
  clearView();
  const paragraph = document.createElement("p");
  paragraph.className = "empty";
  paragraph.textContent = text;
  view.appendChild(paragraph);
}

function renderError(message, retry) {
  setModeVisible(false);
  currentTopic = null;
  finishLoader();
  clearView();
  const box = document.createElement("div");
  box.className = "error";
  const text = document.createElement("p");
  text.textContent = message;
  box.appendChild(text);
  if (retry) {
    const button = document.createElement("button");
    button.textContent = "Повторить";
    button.addEventListener("click", retry);
    box.appendChild(button);
  }
  view.appendChild(box);
}

function renderList(items, onSelect) {
  setModeVisible(false);
  currentTopic = null;
  finishLoader();
  clearView();
  if (!items.length) {
    renderMessage("Пока пусто");
    return;
  }
  const list = document.createElement("div");
  list.className = "list";
  items.forEach((item) => {
    const button = document.createElement("button");
    button.className = "list-item";
    const title = document.createElement("span");
    title.textContent = item.title;
    button.appendChild(title);
    if (item.subtitle) {
      const subtitle = document.createElement("span");
      subtitle.className = "subtitle";
      subtitle.textContent = item.subtitle;
      button.appendChild(subtitle);
    }
    button.addEventListener("click", () => {
      haptic();
      onSelect(item);
    });
    list.appendChild(button);
  });
  view.appendChild(list);
}

async function fetchJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error("HTTP " + response.status);
  return response.json();
}

function loadTree() {
  if (!treePromise) {
    treePromise = fetchJson("/api/tree").catch((error) => {
      treePromise = null;
      throw error;
    });
  }
  return treePromise;
}

function push(screen) {
  nav.stack.push(screen);
  updateBackButton();
}

function updateBackButton() {
  const show = nav.stack.length > 1;
  if (backButton) backButton.hidden = !show;
  if (tg && tg.BackButton) {
    if (show) tg.BackButton.show();
    else tg.BackButton.hide();
  }
}

function goBack() {
  if (nav.stack.length <= 1) return;
  nav.stack.pop();
  nav.stack[nav.stack.length - 1]();
  updateBackButton();
}

async function showTextbooks() {
  setTitle("Физика");
  renderMessage("Загрузка…");
  try {
    const data = await loadTree();
    const items = data.textbooks.map((textbook) => ({
      title: textbook.title,
      subtitle: textbook.author,
      textbook,
    }));
    renderList(items, (item) => {
      push(() => showGrades(item.textbook));
      showGrades(item.textbook);
    });
  } catch (error) {
    renderError("Не удалось загрузить учебники", () => showTextbooks());
  }
}

function openGrade(grade) {
  if (grade.parts && grade.parts.length > 1) {
    showParts(grade);
  } else if (grade.parts && grade.parts.length === 1) {
    showSections(grade.parts[0].sections, grade.parts[0].title);
  } else {
    showSections(grade.sections, grade.title);
  }
}

function showGrades(textbook) {
  setTitle(textbook.title);
  const items = textbook.grades.map((grade) => ({ title: grade.title, grade }));
  renderList(items, (item) => {
    push(() => openGrade(item.grade));
    openGrade(item.grade);
  });
}

function showParts(grade) {
  setTitle(grade.title);
  const items = grade.parts.map((part, index) => ({
    title: part.title,
    subtitle: `Часть ${index + 1}`,
    part,
  }));
  renderList(items, (item) => {
    push(() => showSections(item.part.sections, item.part.title));
    showSections(item.part.sections, item.part.title);
  });
}

function showSections(sections, title) {
  setTitle(title);
  const items = sections.map((section, index) => ({
    title: section.title,
    subtitle: `Глава ${index + 1}`,
    section,
    number: index + 1,
  }));
  renderList(items, (item) => {
    push(() => showTopics(item.section, item.number));
    showTopics(item.section, item.number);
  });
}

function showTopics(section, sectionNumber) {
  setTitle(section.title);
  const items = section.topics.map((topic, index) => ({
    title: `${sectionNumber}.${index + 1}. ${topic.title}`,
    topic,
  }));
  renderList(items, (item) => {
    push(() => showTopic(item.topic.id));
    showTopic(item.topic.id);
  });
}

function renderMath(container) {
  if (window.renderMathInElement) {
    window.renderMathInElement(container, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
      ],
      throwOnError: false,
    });
  }
}

function renderTopic(topic) {
  currentTopic = topic;
  finishLoader();
  setModeVisible(true);
  updateModeButtons();
  setTitle(topic.title);
  clearView();
  const text =
    mode === "retelling" ? topic.retelling || topic.body : topic.body;
  const article = document.createElement("article");
  article.className = "topic";
  article.innerHTML = marked.parse(text);
  view.appendChild(article);
  renderMath(article);
  window.scrollTo(0, 0);
}

async function showTopic(topicId) {
  const cached = topicCache.get(topicId);
  if (cached) {
    renderTopic(cached);
    return;
  }
  renderMessage("Загрузка…");
  try {
    const topic = await fetchJson("/api/topics/" + encodeURIComponent(topicId));
    topicCache.set(topicId, topic);
    renderTopic(topic);
  } catch (error) {
    renderError("Не удалось загрузить тему", () => showTopic(topicId));
  }
}

function showSearch() {
  setTitle("Поиск");
  clearView();
  const form = document.createElement("form");
  form.className = "search";
  const input = document.createElement("input");
  input.type = "search";
  input.placeholder = "Например: скорость";
  const submit = document.createElement("button");
  submit.type = "submit";
  submit.textContent = "Найти";
  form.appendChild(input);
  form.appendChild(submit);
  view.appendChild(form);

  const results = document.createElement("div");
  results.className = "list";
  view.appendChild(results);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = input.value.trim();
    if (!query) return;
    results.innerHTML = "";
    const loading = document.createElement("p");
    loading.className = "empty";
    loading.textContent = "Ищем…";
    results.appendChild(loading);
    try {
      const data = await fetchJson("/api/search?q=" + encodeURIComponent(query));
      results.innerHTML = "";
      if (data.results.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty";
        empty.textContent = "Ничего не найдено";
        results.appendChild(empty);
        return;
      }
      data.results.forEach((result) => {
        const item = document.createElement("button");
        item.className = "list-item";
        const title = document.createElement("span");
        title.textContent = result.title;
        item.appendChild(title);
        const subtitle = document.createElement("span");
        subtitle.className = "subtitle";
        subtitle.textContent = result.textbook_title;
        item.appendChild(subtitle);
        item.addEventListener("click", () => {
          push(() => showTopic(result.topic_id));
          showTopic(result.topic_id);
        });
        results.appendChild(item);
      });
    } catch (error) {
      results.innerHTML = "";
      const text = document.createElement("p");
      text.textContent = "Не удалось выполнить поиск";
      results.appendChild(text);
      const retry = document.createElement("button");
      retry.className = "list-item";
      retry.textContent = "Повторить";
      retry.addEventListener("click", () => form.requestSubmit());
      results.appendChild(retry);
    }
  });
}

if (backButton) backButton.addEventListener("click", goBack);
if (tg && tg.BackButton) tg.BackButton.onClick(goBack);
if (searchButton) {
  searchButton.addEventListener("click", () => {
    push(() => showSearch());
    showSearch();
  });
}

startLoader();
nav.stack.push(() => showTextbooks());
const params = new URLSearchParams(window.location.search);
const deepTopic = params.get("topic");
if (deepTopic) {
  push(() => showTopic(deepTopic));
  showTopic(deepTopic);
} else {
  showTextbooks();
}
updateBackButton();
