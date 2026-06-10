(function () {
  const partialHeader = { "X-Maison-Partial": "filters" };

  function getParts() {
    return {
      form: document.querySelector("[data-filter-form]"),
      results: document.querySelector("[data-filter-results]"),
      chips: document.querySelector("[data-filter-chips]"),
      count: document.querySelector("[data-filter-count]"),
    };
  }

  function buildUrl(form) {
    const formData = new FormData(form);
    const params = new URLSearchParams();
    for (const [key, value] of formData.entries()) {
      const cleanValue = String(value).trim();
      if (cleanValue) {
        params.set(key, cleanValue);
      }
    }
    const url = new URL(form.action, window.location.origin);
    url.search = params.toString();
    return url;
  }

  function skeletonMarkup() {
    return `
      <div class="listing-grid" aria-hidden="true" data-loading-skeleton>
        ${Array.from({ length: 6 })
          .map(
            () => `
              <article class="listing-card listing-card-skeleton">
                <div class="listing-card-media skeleton-block"></div>
                <div class="listing-card-body">
                  <span class="skeleton-line skeleton-line-lg"></span>
                  <span class="skeleton-line"></span>
                  <span class="skeleton-line skeleton-line-sm"></span>
                </div>
              </article>
            `
          )
          .join("")}
      </div>
    `;
  }

  function setLoading(isLoading) {
    const { results } = getParts();
    if (!results) {
      return;
    }
    results.setAttribute("aria-busy", isLoading ? "true" : "false");
    if (isLoading) {
      results.innerHTML = skeletonMarkup();
    }
  }

  function showRecoverableError(message) {
    const { results } = getParts();
    if (!results) {
      return;
    }
    results.setAttribute("aria-busy", "false");
    results.insertAdjacentHTML(
      "afterbegin",
      `<p class="filter-inline-error">${message}</p>`
    );
  }

  async function refresh(url, pushHistory) {
    setLoading(true);
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: partialHeader,
        credentials: "same-origin",
      });
      const payload = await response.json();
      if (!payload.ok) {
        showRecoverableError(payload.error?.message || "Filtres invalides.");
        return;
      }

      const { results, chips, count } = getParts();
      if (results) {
        results.innerHTML = payload.data.results_html;
        results.setAttribute("aria-busy", "false");
      }
      if (chips) {
        chips.outerHTML = payload.data.chips_html;
      }
      if (count) {
        count.textContent = payload.data.result_count_text;
      }
      if (pushHistory) {
        window.history.pushState({}, "", payload.data.url);
      }
    } catch (error) {
      showRecoverableError("Le filtrage a échoué. Essayez Rechercher.");
    }
  }

  function enhanceForm(form) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      refresh(buildUrl(form), true);
    });

    form.addEventListener("change", () => {
      refresh(buildUrl(form), true);
    });
  }

  function enhancePagination() {
    document.addEventListener("click", (event) => {
      const link = event.target.closest("[data-filter-results] .pagination-link");
      if (!link) {
        return;
      }
      event.preventDefault();
      refresh(new URL(link.href), true);
    });
  }

  window.addEventListener("popstate", () => {
    refresh(new URL(window.location.href), false);
  });

  document.addEventListener("DOMContentLoaded", () => {
    const { form } = getParts();
    if (!form || !window.fetch || !window.URLSearchParams) {
      return;
    }
    enhanceForm(form);
    enhancePagination();
  });
})();
