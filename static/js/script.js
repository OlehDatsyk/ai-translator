/**
 * script.js
 * ---------
 * Front-end logic for the AI Translator single-page UI.
 *
 * Responsibilities:
 *   - Call the Flask backend (/api/translate) and render results.
 *   - Manage language dropdowns, swap, copy-to-clipboard.
 *   - Persist and render translation history (localStorage).
 *   - Toggle and persist dark mode.
 *
 * No external libraries are used — plain, dependency-free JavaScript.
 */

(() => {
  "use strict";

  // ------------------------------------------------------------------
  // DOM references
  // ------------------------------------------------------------------
  const sourceLangSelect = document.getElementById("source-lang");
  const targetLangSelect = document.getElementById("target-lang");
  const swapBtn = document.getElementById("swap-btn");

  const sourceTextArea = document.getElementById("source-text");
  const targetTextDiv = document.getElementById("target-text");
  const sourceCharCount = document.getElementById("source-char-count");
  const clearBtn = document.getElementById("clear-btn");
  const copyBtn = document.getElementById("copy-btn");
  const detectedLangBadge = document.getElementById("detected-lang-badge");

  const temperatureSlider = document.getElementById("temperature");
  const temperatureValue = document.getElementById("temperature-value");

  const translateBtn = document.getElementById("translate-btn");
  const translateBtnText = document.getElementById("translate-btn-text");
  const translateSpinner = document.getElementById("translate-spinner");
  const errorBanner = document.getElementById("error-banner");

  const historyList = document.getElementById("history-list");
  const historyEmpty = document.getElementById("history-empty");
  const historyItemTemplate = document.getElementById("history-item-template");
  const clearHistoryBtn = document.getElementById("clear-history-btn");

  const themeToggleBtn = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");

  const MAX_CHARS = 5000;
  const HISTORY_STORAGE_KEY = "ai-translator-history";
  const THEME_STORAGE_KEY = "ai-translator-theme";
  const MAX_HISTORY_ITEMS = 50;

  // ------------------------------------------------------------------
  // Dark mode
  // ------------------------------------------------------------------
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    themeIcon.textContent = theme === "dark" ? "☀️" : "🌙";
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }

  function initTheme() {
    const stored = localStorage.getItem(THEME_STORAGE_KEY);
    if (stored) {
      applyTheme(stored);
      return;
    }
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(prefersDark ? "dark" : "light");
  }

  themeToggleBtn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    applyTheme(current === "dark" ? "light" : "dark");
  });

  // ------------------------------------------------------------------
  // Character counter
  // ------------------------------------------------------------------
  sourceTextArea.addEventListener("input", () => {
    const length = sourceTextArea.value.length;
    sourceCharCount.textContent = `${length} / ${MAX_CHARS}`;
    sourceCharCount.style.color =
      length >= MAX_CHARS ? "var(--color-danger)" : "var(--color-text-muted)";
  });

  // ------------------------------------------------------------------
  // Temperature slider
  // ------------------------------------------------------------------
  temperatureSlider.addEventListener("input", () => {
    temperatureValue.textContent = Number(temperatureSlider.value).toFixed(1);
  });

  // ------------------------------------------------------------------
  // Swap languages
  // ------------------------------------------------------------------
  swapBtn.addEventListener("click", () => {
    const sourceValue = sourceLangSelect.value;
    const targetValue = targetLangSelect.value;

    // Can't swap into "Auto Detect" on the target side, and the source
    // side should not literally mirror "Auto Detect" as a real language.
    if (sourceValue === "Auto Detect") {
      showError("Select a specific source language before swapping.");
      return;
    }

    sourceLangSelect.value = targetValue;
    targetLangSelect.value = sourceValue;

    // Swap the text content too, if there is a translation to swap in.
    const currentTranslation = targetTextDiv.textContent.trim();
    if (currentTranslation) {
      sourceTextArea.value = currentTranslation;
      targetTextDiv.textContent = "";
      sourceCharCount.textContent = `${sourceTextArea.value.length} / ${MAX_CHARS}`;
    }
  });

  // ------------------------------------------------------------------
  // Clear
  // ------------------------------------------------------------------
  clearBtn.addEventListener("click", () => {
    sourceTextArea.value = "";
    targetTextDiv.textContent = "";
    detectedLangBadge.classList.add("hidden");
    sourceCharCount.textContent = `0 / ${MAX_CHARS}`;
    hideError();
    sourceTextArea.focus();
  });

  // ------------------------------------------------------------------
  // Copy to clipboard
  // ------------------------------------------------------------------
  copyBtn.addEventListener("click", async () => {
    const text = targetTextDiv.textContent;
    if (!text.trim()) {
      return;
    }
    try {
      await navigator.clipboard.writeText(text);
      const original = copyBtn.textContent;
      copyBtn.textContent = "✅ Copied";
      setTimeout(() => {
        copyBtn.textContent = original;
      }, 1500);
    } catch (err) {
      showError("Could not copy text to clipboard.");
    }
  });

  // ------------------------------------------------------------------
  // Error banner helpers
  // ------------------------------------------------------------------
  function showError(message) {
    errorBanner.textContent = message;
    errorBanner.classList.remove("hidden");
  }

  function hideError() {
    errorBanner.classList.add("hidden");
    errorBanner.textContent = "";
  }

  // ------------------------------------------------------------------
  // Translate action
  // ------------------------------------------------------------------
  async function translate() {
    const text = sourceTextArea.value.trim();
    const targetLanguage = targetLangSelect.value;
    const sourceLanguage = sourceLangSelect.value;
    const temperature = Number(temperatureSlider.value);

    hideError();

    if (!text) {
      showError("Please enter some text to translate.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text,
          target_language: targetLanguage,
          source_language: sourceLanguage,
          temperature,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Translation failed. Please try again.");
      }

      renderTranslation(data);
      saveToHistory({
        sourceText: text,
        translatedText: data.translated_text,
        sourceLanguage: sourceLanguage === "Auto Detect"
          ? data.detected_source_language
          : sourceLanguage,
        targetLanguage,
        timestamp: Date.now(),
      });
    } catch (err) {
      showError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function renderTranslation(data) {
    targetTextDiv.textContent = data.translated_text;

    if (sourceLangSelect.value === "Auto Detect" && data.detected_source_language) {
      detectedLangBadge.textContent = `Detected: ${data.detected_source_language}`;
      detectedLangBadge.classList.remove("hidden");
    } else {
      detectedLangBadge.classList.add("hidden");
    }
  }

  function setLoading(isLoading) {
    translateBtn.disabled = isLoading;
    translateSpinner.classList.toggle("hidden", !isLoading);
    translateBtnText.textContent = isLoading ? "Translating..." : "Translate";
  }

  translateBtn.addEventListener("click", translate);

  // Allow Ctrl+Enter / Cmd+Enter to trigger translation from the textarea.
  sourceTextArea.addEventListener("keydown", (event) => {
    const isSubmitCombo = (event.ctrlKey || event.metaKey) && event.key === "Enter";
    if (isSubmitCombo) {
      event.preventDefault();
      translate();
    }
  });

  // ------------------------------------------------------------------
  // History (persisted to localStorage)
  // ------------------------------------------------------------------
  function loadHistory() {
    try {
      const raw = localStorage.getItem(HISTORY_STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (err) {
      console.error("Failed to parse translation history:", err);
      return [];
    }
  }

  function persistHistory(history) {
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(history));
  }

  function saveToHistory(entry) {
    const history = loadHistory();
    history.unshift({ id: crypto.randomUUID(), ...entry });
    const trimmed = history.slice(0, MAX_HISTORY_ITEMS);
    persistHistory(trimmed);
    renderHistory();
  }

  function deleteHistoryItem(id) {
    const history = loadHistory().filter((item) => item.id !== id);
    persistHistory(history);
    renderHistory();
  }

  function formatRelativeTime(timestamp) {
    const diffSeconds = Math.round((Date.now() - timestamp) / 1000);
    if (diffSeconds < 60) return "just now";
    const diffMinutes = Math.round(diffSeconds / 60);
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    const diffHours = Math.round(diffMinutes / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    const diffDays = Math.round(diffHours / 24);
    return `${diffDays}d ago`;
  }

  function renderHistory() {
    const history = loadHistory();
    historyList.querySelectorAll(".history-item").forEach((el) => el.remove());

    if (history.length === 0) {
      historyEmpty.classList.remove("hidden");
      return;
    }
    historyEmpty.classList.add("hidden");

    history.forEach((entry) => {
      const fragment = historyItemTemplate.content.cloneNode(true);
      const li = fragment.querySelector(".history-item");

      fragment.querySelector(".history-langs").textContent =
        `${entry.sourceLanguage} → ${entry.targetLanguage}`;
      fragment.querySelector(".history-time").textContent =
        formatRelativeTime(entry.timestamp);
      fragment.querySelector(".history-source").textContent = entry.sourceText;
      fragment.querySelector(".history-target").textContent = entry.translatedText;

      fragment.querySelector(".reuse-btn").addEventListener("click", () => {
        sourceTextArea.value = entry.sourceText;
        sourceCharCount.textContent = `${entry.sourceText.length} / ${MAX_CHARS}`;
        targetTextDiv.textContent = entry.translatedText;
        setSelectValueIfPresent(targetLangSelect, entry.targetLanguage);
        window.scrollTo({ top: 0, behavior: "smooth" });
      });

      fragment.querySelector(".delete-btn").addEventListener("click", () => {
        deleteHistoryItem(entry.id);
      });

      historyList.appendChild(li);
    });
  }

  function setSelectValueIfPresent(selectEl, value) {
    const optionExists = Array.from(selectEl.options).some(
      (opt) => opt.value === value
    );
    if (optionExists) {
      selectEl.value = value;
    }
  }

  clearHistoryBtn.addEventListener("click", () => {
    persistHistory([]);
    renderHistory();
  });

  // ------------------------------------------------------------------
  // Init
  // ------------------------------------------------------------------
  initTheme();
  renderHistory();
})();
