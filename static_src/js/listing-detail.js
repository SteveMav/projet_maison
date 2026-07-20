document.addEventListener("DOMContentLoaded", () => {
  const dialog = document.getElementById("detail-drawer");
  let lastTriggerElement = null;
  const favoritesKey = "maison.favoriteListings";

  // Helper to check if screen is desktop
  function isDesktop() {
    return window.matchMedia("(min-width: 700px)").matches;
  }

  function readFavorites() {
    try {
      return new Set(JSON.parse(window.localStorage.getItem(favoritesKey) || "[]"));
    } catch (error) {
      return new Set();
    }
  }

  function writeFavorites(favorites) {
    window.localStorage.setItem(favoritesKey, JSON.stringify([...favorites]));
  }

  function refreshFavoriteButtons() {
    const favorites = readFavorites();
    document.querySelectorAll("[data-favorite-listing]").forEach((button) => {
      const listingId = button.dataset.favoriteListing;
      const isFavorite = favorites.has(listingId);
      button.setAttribute("aria-pressed", isFavorite ? "true" : "false");
      button.setAttribute(
        "aria-label",
        isFavorite ? "Retirer cette annonce des favoris" : "Ajouter cette annonce aux favoris"
      );
      const icon = button.querySelector("[aria-hidden='true']");
      if (icon) {
        icon.textContent = isFavorite ? "♥" : "♡";
      }
    });
  }

  // Intercept click on listing card links for desktop drawer view
  document.addEventListener("click", async (e) => {
    const cardLink = e.target.closest(".listing-card-link");
    if (!cardLink || !dialog) return;

    if (isDesktop()) {
      e.preventDefault();
      lastTriggerElement = cardLink;

      // Prepare from parameter to preserve browse context
      const fromUrl = window.location.pathname + window.location.search;
      const targetUrl = new URL(cardLink.href);
      targetUrl.searchParams.set("from", fromUrl);

      // Fetch partial content
      try {
        const response = await fetch(targetUrl.toString(), {
          headers: {
            "X-Maison-Partial": "listing-detail",
          },
        });

        if (!response.ok) {
          throw new Error("Erreur de chargement du détail de l'annonce.");
        }

        const html = await response.text();
        dialog.innerHTML = html;
        refreshFavoriteButtons();

        // Apply inert to main and header
        const header = document.querySelector(".site-header");
        const main = document.getElementById("main");
        if (header) header.setAttribute("inert", "");
        if (main) main.setAttribute("inert", "");

        dialog.showModal();
        
        // Focus close button inside the drawer or the dialog itself
        const closeBtn = dialog.querySelector("[data-close-drawer]");
        if (closeBtn) {
          closeBtn.focus();
        }
      } catch (err) {
        console.error(err);
        alert("Impossible de charger les détails de l'annonce.");
      }
    }
  });

  // Handle drawer close
  function closeDrawer() {
    if (!dialog || !dialog.open) return;
    dialog.close();
  }

  if (dialog) {
    dialog.addEventListener("close", () => {
      // Remove inert attributes
      const header = document.querySelector(".site-header");
      const main = document.getElementById("main");
      if (header) header.removeAttribute("inert");
      if (main) main.removeAttribute("inert");

      // Restore focus
      if (lastTriggerElement) {
        lastTriggerElement.focus();
        lastTriggerElement = null;
      }
    });

    // Close on clicking backdrop
    dialog.addEventListener("click", (e) => {
      const rect = dialog.getBoundingClientRect();
      const isInDialog = (
        e.clientX >= rect.left &&
        e.clientX <= rect.right &&
        e.clientY >= rect.top &&
        e.clientY <= rect.bottom
      );
      if (!isInDialog) {
        closeDrawer();
      }
    });
  }

  // Handle close button click inside drawer
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-close-drawer]")) {
      closeDrawer();
    }
  });

  document.addEventListener("click", async (e) => {
    const favoriteButton = e.target.closest("[data-favorite-listing]");
    if (favoriteButton) {
      e.preventDefault();
      const favorites = readFavorites();
      const listingId = favoriteButton.dataset.favoriteListing;
      if (favorites.has(listingId)) {
        favorites.delete(listingId);
      } else {
        favorites.add(listingId);
      }
      writeFavorites(favorites);
      refreshFavoriteButtons();
      return;
    }

    const shareButton = e.target.closest("[data-share-listing]");
    if (shareButton) {
      e.preventDefault();
      const title = document.title || "Annonce Maison";
      const url = window.location.href;
      if (navigator.share) {
        try {
          await navigator.share({ title, url });
        } catch (error) {
          // User cancellation is not an error state for the interface.
        }
      } else if (navigator.clipboard) {
        await navigator.clipboard.writeText(url);
        shareButton.dataset.copied = "true";
        window.setTimeout(() => {
          delete shareButton.dataset.copied;
        }, 1800);
      }
    }
  });

  // Gallery thumbnail click handler using event delegation
  document.addEventListener("click", (e) => {
    const thumb = e.target.closest("[data-gallery-thumb]");
    if (!thumb) return;

    e.preventDefault();
    const gallery = thumb.closest("[data-gallery]");
    if (!gallery) return;

    const mainImage = gallery.querySelector("[data-gallery-main]");
    const countLabel = gallery.querySelector("[data-gallery-count]");
    const allThumbs = gallery.querySelectorAll("[data-gallery-thumb]");

    if (mainImage) {
      mainImage.src = thumb.dataset.src;
      mainImage.alt = thumb.dataset.alt;
    }

    allThumbs.forEach((t) => t.classList.remove("active"));
    thumb.classList.add("active");

    if (countLabel) {
      countLabel.textContent = `${thumb.dataset.index}/${allThumbs.length}`;
    }
  });

  refreshFavoriteButtons();
});
