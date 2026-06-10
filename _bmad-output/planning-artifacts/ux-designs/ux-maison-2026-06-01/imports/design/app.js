const listings = [
  {
    id: "M-1048",
    title: "Appartement traversant avec balcon",
    commune: "Gombe",
    neighborhood: "Socimat",
    bedrooms: 2,
    bathrooms: 2,
    type: "Appartement",
    price: 980,
    verified: true,
    updated: "Mise à jour aujourd’hui",
    views: 184,
    image: "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg?auto=compress&cs=tinysrgb&w=900",
    gallery: [
      "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg?auto=compress&cs=tinysrgb&w=1200",
      "https://images.pexels.com/photos/276724/pexels-photo-276724.jpeg?auto=compress&cs=tinysrgb&w=700",
      "https://images.pexels.com/photos/1457842/pexels-photo-1457842.jpeg?auto=compress&cs=tinysrgb&w=700",
    ],
    description:
      "Appartement lumineux avec séjour traversant, balcon protégé et accès rapide au boulevard. Les pièces principales sont ventilées et les photos ont été contrôlées lors de la publication.",
    agent: "Patrick Ilunga",
    agentInitials: "PI",
  },
  {
    id: "M-1036",
    title: "Maison calme avec jardin arboré",
    commune: "Ngaliema",
    neighborhood: "Ma Campagne",
    bedrooms: 3,
    bathrooms: 2,
    type: "Maison",
    price: 1350,
    verified: true,
    updated: "Mise à jour hier",
    views: 247,
    image: "https://images.pexels.com/photos/1642125/pexels-photo-1642125.jpeg?auto=compress&cs=tinysrgb&w=900",
    gallery: [
      "https://images.pexels.com/photos/1642125/pexels-photo-1642125.jpeg?auto=compress&cs=tinysrgb&w=1200",
      "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg?auto=compress&cs=tinysrgb&w=700",
      "https://images.pexels.com/photos/1643383/pexels-photo-1643383.jpeg?auto=compress&cs=tinysrgb&w=700",
    ],
    description:
      "Maison familiale en retrait de la route avec une cour agréable et trois chambres bien distribuées. La disponibilité a été reconfirmée hier avec le commissionnaire.",
    agent: "Patrick Ilunga",
    agentInitials: "PI",
  },
  {
    id: "M-1029",
    title: "Deux chambres rénové, cour partagée",
    commune: "Limete",
    neighborhood: "Résidentiel",
    bedrooms: 2,
    bathrooms: 1,
    type: "Appartement",
    price: 640,
    verified: false,
    updated: "Mise à jour il y a 2 jours",
    views: 91,
    image: "https://images.pexels.com/photos/1918291/pexels-photo-1918291.jpeg?auto=compress&cs=tinysrgb&w=900",
    gallery: [
      "https://images.pexels.com/photos/1918291/pexels-photo-1918291.jpeg?auto=compress&cs=tinysrgb&w=1200",
      "https://images.pexels.com/photos/1571459/pexels-photo-1571459.jpeg?auto=compress&cs=tinysrgb&w=700",
      "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&w=700",
    ],
    description:
      "Appartement rénové adapté à un couple ou une petite famille. Les pièces sont simples, propres et faciles à meubler. Cette annonce respecte le standard de publication Maison sans badge de vérification supplémentaire.",
    agent: "Espérance Mbuyi",
    agentInitials: "EM",
  },
  {
    id: "M-1022",
    title: "Studio meublé proche des commerces",
    commune: "Kintambo",
    neighborhood: "Magasin",
    bedrooms: 1,
    bathrooms: 1,
    type: "Studio",
    price: 420,
    verified: false,
    updated: "Mise à jour il y a 3 jours",
    views: 68,
    image: "https://images.pexels.com/photos/1454806/pexels-photo-1454806.jpeg?auto=compress&cs=tinysrgb&w=900",
    gallery: [
      "https://images.pexels.com/photos/1454806/pexels-photo-1454806.jpeg?auto=compress&cs=tinysrgb&w=1200",
      "https://images.pexels.com/photos/271816/pexels-photo-271816.jpeg?auto=compress&cs=tinysrgb&w=700",
      "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&w=700",
    ],
    description:
      "Studio meublé à quelques minutes des commerces de Kintambo. Une option pratique pour une personne seule qui souhaite s’installer rapidement.",
    agent: "Junior Banza",
    agentInitials: "JB",
  },
  {
    id: "M-1014",
    title: "Maison familiale avec grande cour",
    commune: "Lemba",
    neighborhood: "Salongo",
    bedrooms: 4,
    bathrooms: 2,
    type: "Maison",
    price: 760,
    verified: true,
    updated: "Mise à jour il y a 4 jours",
    views: 133,
    image: "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg?auto=compress&cs=tinysrgb&w=900",
    gallery: [
      "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg?auto=compress&cs=tinysrgb&w=1200",
      "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=700",
      "https://images.pexels.com/photos/534151/pexels-photo-534151.jpeg?auto=compress&cs=tinysrgb&w=700",
    ],
    description:
      "Maison pensée pour une famille avec une grande cour, quatre chambres et un espace extérieur facile à aménager. Le contact commissionnaire et les médias ont passé le contrôle renforcé Maison.",
    agent: "Rachel Kiese",
    agentInitials: "RK",
  },
  {
    id: "M-1007",
    title: "Appartement compact avec terrasse",
    commune: "Bandalungwa",
    neighborhood: "Moulaert",
    bedrooms: 2,
    bathrooms: 1,
    type: "Appartement",
    price: 520,
    verified: false,
    updated: "Mise à jour il y a 5 jours",
    views: 74,
    image: "https://images.pexels.com/photos/1571453/pexels-photo-1571453.jpeg?auto=compress&cs=tinysrgb&w=900",
    gallery: [
      "https://images.pexels.com/photos/1571453/pexels-photo-1571453.jpeg?auto=compress&cs=tinysrgb&w=1200",
      "https://images.pexels.com/photos/2082087/pexels-photo-2082087.jpeg?auto=compress&cs=tinysrgb&w=700",
      "https://images.pexels.com/photos/2029670/pexels-photo-2029670.jpeg?auto=compress&cs=tinysrgb&w=700",
    ],
    description:
      "Deux chambres compactes et une terrasse agréable pour profiter de la fin de journée. La fiche est récente et peut être signalée facilement si la disponibilité ne correspond plus au terrain.",
    agent: "Grâce Matondo",
    agentInitials: "GM",
  },
];

const state = {
  favorites: new Set(),
  filters: {
    commune: "",
    budget: "",
    bedrooms: "",
  },
};

const listingGrid = document.querySelector("#listing-grid");
const emptyState = document.querySelector("#empty-state");
const resultCount = document.querySelector("#result-count");
const activeFilters = document.querySelector("#active-filters");
const filterPanel = document.querySelector("#filter-panel");
const filterButton = document.querySelector("#filter-button");
const communeFilter = document.querySelector("#commune-filter");
const budgetFilter = document.querySelector("#budget-filter");
const bedroomFilter = document.querySelector("#bedroom-filter");
const detailPanel = document.querySelector("#detail-panel");
const detailBody = document.querySelector("#detail-body");
const pageScrim = document.querySelector("#page-scrim");
const leadDialog = document.querySelector("#lead-dialog");
const leadForm = document.querySelector("#lead-form");
const toastRegion = document.querySelector("#toast-region");

function icon(name) {
  return `<svg class="icon" aria-hidden="true"><use href="#icon-${name}"></use></svg>`;
}

function formatPrice(value) {
  return new Intl.NumberFormat("fr-FR").format(value);
}

function verifiedMarkup(listing, compact = false) {
  if (!listing.verified) {
    return "";
  }

  if (compact) {
    return `<span class="card-badge">${icon("shield")} Vérifiée</span>`;
  }

  return `
    <div class="trust-box">
      ${icon("shield")}
      <div>
        <h3>Annonce vérifiée</h3>
        <p>Cette annonce a passé un contrôle supplémentaire. Le badge ne garantit pas le résultat d’une transaction hors ligne.</p>
      </div>
    </div>
  `;
}

function listingCard(listing, index) {
  const favorite = state.favorites.has(listing.id);
  return `
    <article class="listing-card" style="--index: ${index}">
      <button class="listing-main-button" type="button" data-listing-id="${listing.id}" aria-label="Voir ${listing.title}">
        <div class="listing-image-wrap">
          <img src="${listing.image}" alt="${listing.title}" loading="lazy" />
          <div class="listing-image-top">${verifiedMarkup(listing, true)}</div>
        </div>
        <div class="listing-body">
          <p class="listing-kicker">${listing.commune} · ${listing.neighborhood}</p>
          <h3>${listing.title}</h3>
          <div class="listing-meta">
            <span>${icon("bed")} ${listing.bedrooms} chambre${listing.bedrooms > 1 ? "s" : ""}</span>
            <span>${icon("building")} ${listing.type}</span>
          </div>
          <div class="listing-bottom">
            <p class="listing-price">$${formatPrice(listing.price)}<span>/ mois</span></p>
            <p class="listing-updated">${icon("clock")} ${listing.updated.replace("Mise à jour ", "")}</p>
          </div>
        </div>
      </button>
      <button
        class="favorite-button ${favorite ? "is-favorite" : ""}"
        type="button"
        data-favorite-id="${listing.id}"
        aria-label="${favorite ? "Retirer des favoris" : "Ajouter aux favoris"}"
        aria-pressed="${favorite}"
      >
        ${icon("heart")}
      </button>
    </article>
  `;
}

function skeletons() {
  return Array.from(
    { length: 6 },
    () => `
      <article class="listing-skeleton" aria-hidden="true">
        <div class="skeleton-block skeleton-image"></div>
        <div class="skeleton-block skeleton-line"></div>
        <div class="skeleton-block skeleton-line"></div>
        <div class="skeleton-block skeleton-line"></div>
      </article>
    `,
  ).join("");
}

function matchingListings() {
  return listings.filter((listing) => {
    const hasCommune = !state.filters.commune || listing.commune === state.filters.commune;
    const fitsBudget = !state.filters.budget || listing.price <= Number(state.filters.budget);
    const hasBedrooms = !state.filters.bedrooms || listing.bedrooms >= Number(state.filters.bedrooms);
    return hasCommune && fitsBudget && hasBedrooms;
  });
}

function renderListings(filteredListings = matchingListings()) {
  listingGrid.innerHTML = filteredListings.map(listingCard).join("");
  resultCount.textContent = `${filteredListings.length} bien${filteredListings.length > 1 ? "s" : ""} disponible${filteredListings.length > 1 ? "s" : ""}`;
  emptyState.hidden = filteredListings.length !== 0;
  listingGrid.hidden = filteredListings.length === 0;
  renderActiveFilters();
}

function renderActiveFilters() {
  const items = [];
  if (state.filters.commune) {
    items.push({ key: "commune", label: state.filters.commune });
  }
  if (state.filters.budget) {
    items.push({ key: "budget", label: `Max. $${formatPrice(state.filters.budget)}` });
  }
  if (state.filters.bedrooms) {
    items.push({ key: "bedrooms", label: `${state.filters.bedrooms}+ chambres` });
  }

  activeFilters.innerHTML = items
    .map(
      (item) => `
        <span class="active-filter">
          ${item.label}
          <button type="button" data-clear-filter="${item.key}" aria-label="Retirer le filtre ${item.label}">
            ${icon("x")}
          </button>
        </span>
      `,
    )
    .join("");

  document.querySelectorAll("[data-commune]").forEach((chip) => {
    chip.classList.toggle("is-selected", chip.dataset.commune === state.filters.commune);
  });
}

function showLoadingThenRender() {
  listingGrid.hidden = false;
  emptyState.hidden = true;
  listingGrid.innerHTML = skeletons();
  resultCount.textContent = "Recherche des annonces disponibles…";
  window.setTimeout(() => renderListings(), 460);
}

function syncFiltersFromControls() {
  state.filters.commune = communeFilter.value;
  state.filters.budget = budgetFilter.value;
  state.filters.bedrooms = bedroomFilter.value;
}

function syncControlsFromFilters() {
  communeFilter.value = state.filters.commune;
  budgetFilter.value = state.filters.budget;
  bedroomFilter.value = state.filters.bedrooms;
}

function resetFilters() {
  state.filters = { commune: "", budget: "", bedrooms: "" };
  syncControlsFromFilters();
  showLoadingThenRender();
}

function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `${icon("check")}<span>${message}</span>`;
  toastRegion.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add("is-visible"));

  window.setTimeout(() => {
    toast.classList.remove("is-visible");
    window.setTimeout(() => toast.remove(), 220);
  }, 3200);
}

function openDetail(listingId) {
  const listing = listings.find((item) => item.id === listingId);
  if (!listing) {
    return;
  }

  detailBody.innerHTML = `
    <div class="detail-gallery">
      ${listing.gallery.map((source) => `<img src="${source}" alt="" />`).join("")}
    </div>
    <div class="detail-content">
      <p class="eyebrow">${listing.commune} · ${listing.neighborhood}</p>
      <h2 id="detail-title">${listing.title}</h2>
      <p class="detail-price">$${formatPrice(listing.price)}<span>/ mois</span></p>

      <div class="detail-facts">
        <article><span>Chambres</span><strong>${listing.bedrooms}</strong></article>
        <article><span>Douches</span><strong>${listing.bathrooms}</strong></article>
        <article><span>Vues</span><strong>${listing.views}</strong></article>
      </div>

      ${verifiedMarkup(listing)}

      <section class="detail-section">
        <h3>À propos de ce bien</h3>
        <p>${listing.description}</p>
      </section>

      <section class="detail-section">
        <h3>Disponibilité</h3>
        <p>${listing.updated}. La disponibilité peut encore évoluer avant votre échange avec le commissionnaire.</p>
      </section>

      <section class="detail-section">
        <h3>Commissionnaire</h3>
        <div class="agent-row">
          <span class="agent-avatar">${listing.agentInitials}</span>
          <div>
            <strong>${listing.agent}</strong>
            <p>Contact WhatsApp transmis après identification légère.</p>
          </div>
        </div>
      </section>

      <button class="text-button" type="button" data-report-listing="${listing.id}">
        Signaler cette annonce
      </button>
    </div>
    <div class="detail-actions">
      <button class="button button-primary" type="button" data-contact-listing="${listing.id}">
        ${icon("message")}
        Contacter sur WhatsApp
      </button>
      <button class="button button-secondary" type="button" data-toast="Annonce ajoutée aux favoris.">
        ${icon("heart")}
        Favori
      </button>
    </div>
  `;

  pageScrim.hidden = false;
  document.body.classList.add("is-locked");
  detailPanel.setAttribute("aria-hidden", "false");
  detailPanel.removeAttribute("inert");
  void detailPanel.offsetWidth;
  pageScrim.classList.add("is-visible");
  detailPanel.classList.add("is-open");
}

function closeDetail() {
  detailPanel.classList.remove("is-open");
  pageScrim.classList.remove("is-visible");
  detailPanel.setAttribute("aria-hidden", "true");
  detailPanel.setAttribute("inert", "");
  window.setTimeout(() => {
    pageScrim.hidden = true;
    document.body.classList.remove("is-locked");
    if (!detailPanel.classList.contains("is-open")) {
      detailBody.innerHTML = "";
    }
  }, 260);
}

function showView(viewName) {
  const tenantView = document.querySelector("#tenant-view");
  const proView = document.querySelector("#pro-view");
  const isTenant = viewName === "tenant";

  tenantView.hidden = !isTenant;
  proView.hidden = isTenant;
  tenantView.classList.toggle("is-visible", isTenant);
  proView.classList.toggle("is-visible", !isTenant);
  document.querySelectorAll("[data-view-target='tenant']").forEach((button) => {
    button.classList.toggle("is-active", isTenant && button.closest(".mobile-bottom-nav"));
  });
  document.querySelectorAll("[data-view-target='pro']").forEach((button) => {
    button.classList.toggle("is-active", !isTenant && button.closest(".mobile-bottom-nav"));
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

document.querySelector("#search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  syncFiltersFromControls();
  showLoadingThenRender();
});

filterButton.addEventListener("click", () => {
  const willOpen = filterPanel.hidden;
  filterPanel.hidden = !willOpen;
  filterButton.setAttribute("aria-expanded", String(willOpen));
});

document.querySelector("#commune-chips").addEventListener("click", (event) => {
  const chip = event.target.closest("[data-commune]");
  if (!chip) {
    return;
  }
  state.filters.commune = state.filters.commune === chip.dataset.commune ? "" : chip.dataset.commune;
  syncControlsFromFilters();
  showLoadingThenRender();
});

activeFilters.addEventListener("click", (event) => {
  const clearButton = event.target.closest("[data-clear-filter]");
  if (!clearButton) {
    return;
  }
  state.filters[clearButton.dataset.clearFilter] = "";
  syncControlsFromFilters();
  showLoadingThenRender();
});

listingGrid.addEventListener("click", (event) => {
  const favoriteButton = event.target.closest("[data-favorite-id]");
  if (favoriteButton) {
    const listingId = favoriteButton.dataset.favoriteId;
    if (state.favorites.has(listingId)) {
      state.favorites.delete(listingId);
      showToast("Annonce retirée des favoris.");
    } else {
      state.favorites.add(listingId);
      showToast("Annonce ajoutée aux favoris.");
    }
    renderListings();
    return;
  }

  const listingButton = event.target.closest("[data-listing-id]");
  if (listingButton) {
    openDetail(listingButton.dataset.listingId);
  }
});

detailBody.addEventListener("click", (event) => {
  const contactButton = event.target.closest("[data-contact-listing]");
  if (contactButton) {
    leadDialog.showModal();
    return;
  }

  const reportButton = event.target.closest("[data-report-listing]");
  if (reportButton) {
    showToast("Signalement préparé. Merci de contribuer à la fiabilité des annonces.");
  }
});

document.querySelectorAll("[data-toast]").forEach((button) => {
  button.addEventListener("click", () => showToast(button.dataset.toast));
});

document.querySelectorAll("[data-view-target]").forEach((button) => {
  button.addEventListener("click", (event) => {
    event.preventDefault();
    closeDetail();
    showView(button.dataset.viewTarget);
  });
});

document.querySelector("#detail-close").addEventListener("click", closeDetail);
document.querySelector("#lead-close").addEventListener("click", () => leadDialog.close());
document.querySelector("#reset-filters").addEventListener("click", resetFilters);
document.querySelector("#empty-reset").addEventListener("click", resetFilters);
pageScrim.addEventListener("click", closeDetail);

leadForm.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!leadForm.reportValidity()) {
    return;
  }
  leadDialog.close();
  closeDetail();
  leadForm.reset();
  showToast("Lead créé. Le passage vers WhatsApp est prêt.");
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && detailPanel.classList.contains("is-open") && !leadDialog.open) {
    closeDetail();
  }
});

renderListings();
