document.addEventListener("DOMContentLoaded", () => {
  let lastTriggerElement = null;

  // Helper to get CSRF token from cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function showStatus(element) {
    if (!element) return;
    element.hidden = false;
    element.style.display = "";
  }

  function hideStatus(element) {
    if (!element) return;
    element.hidden = true;
    element.style.display = "";
  }

  // Event delegation to capture clicks on all WhatsApp buttons
  document.addEventListener("click", async (e) => {
    const button = e.target.closest("[data-contact-whatsapp]");
    if (!button) return;

    const isAuthenticated = button.dataset.userAuthenticated === "true";
    const idRequired = button.dataset.idRequired === "true";

    if (!isAuthenticated) {
      // User is not signed in: redirect to login page
      e.preventDefault();
      const nextUrl = window.location.pathname + window.location.search;
      window.location.href = `/accounts/login/?next=${encodeURIComponent(nextUrl)}`;
      return;
    }

    e.preventDefault();
    if (idRequired) {
      // User needs lightweight identification: open the modal
      lastTriggerElement = button;
      openIdentificationModal();
    } else {
      // User already identified/consented: proceed with Lead creation
      triggerLeadCreation(button);
    }
  });

  function openIdentificationModal() {
    const modal = document.getElementById("identification-modal");
    if (!modal) return;

    // Open the modal natively
    modal.showModal();

    // Focus on first name input
    const firstNameInput = document.getElementById("id_first_name");
    if (firstNameInput) {
      firstNameInput.focus();
    }

    // Set up form submission handler
    const form = document.getElementById("identification-form");
    if (form) {
      form.addEventListener("submit", handleFormSubmit);
    }

    // Set up close button handler
    const closeBtn = modal.querySelector("[data-close-modal]");
    if (closeBtn) {
      closeBtn.addEventListener("click", closeIdentificationModal);
    }
  }

  function closeIdentificationModal() {
    const modal = document.getElementById("identification-modal");
    if (!modal) return;

    modal.close();

    // Clean form listener
    const form = document.getElementById("identification-form");
    if (form) {
      form.removeEventListener("submit", handleFormSubmit);
    }

    // Restore focus
    if (lastTriggerElement) {
      lastTriggerElement.focus();
      lastTriggerElement = null;
    }
  }

  async function handleFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector(".modal-submit-btn");
    const modalErrorContainer = document.getElementById("handoff-error-modal");
    const modalErrorText = modalErrorContainer ? modalErrorContainer.querySelector(".error-text") : null;

    // Clear previous errors
    if (modalErrorContainer) {
      hideStatus(modalErrorContainer);
    }
    if (modalErrorText) {
      modalErrorText.textContent = "";
    }
    form.querySelectorAll(".error-msg").forEach((span) => (span.textContent = ""));
    form.querySelectorAll(".form-input, .form-checkbox").forEach((el) => {
      el.classList.remove("is-invalid");
      el.removeAttribute("aria-invalid");
    });

    // Save previous button state and set to loading
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;

    // Dot animation on modal submit button
    let dotCount = 0;
    submitBtn.textContent = "Envoi en cours";
    const submitInterval = setInterval(() => {
      dotCount = (dotCount + 1) % 4;
      submitBtn.textContent = "Envoi en cours" + ".".repeat(dotCount);
    }, 400);

    const formData = new FormData(form);

    try {
      // Step 1: Submit identification
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Success: update all CTA buttons in the DOM to avoid prompting again
          document.querySelectorAll("[data-contact-whatsapp]").forEach((btn) => {
            btn.dataset.idRequired = "false";
          });

          // Step 2: Since identification succeeded, trigger lead creation while keeping modal open
          if (lastTriggerElement) {
            const listingId = lastTriggerElement.dataset.listingId;
            // Update modal submit button text to indicate lead creation
            clearInterval(submitInterval);
            submitBtn.textContent = "Création du contact...";
            
            const leadSuccess = await executeLeadCreation(listingId);
            if (leadSuccess) {
              closeIdentificationModal();
            } else {
              // Lead creation failed: stop loading, keep modal open
              clearInterval(submitInterval);
              submitBtn.textContent = originalText;
              submitBtn.disabled = false;
            }
          } else {
            closeIdentificationModal();
            clearInterval(submitInterval);
          }
        }
      } else if (response.status === 400) {
        clearInterval(submitInterval);
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;

        const data = await response.json();
        if (data.errors) {
          let firstErroneousInput = null;

          for (const [fieldName, errorList] of Object.entries(data.errors)) {
            const errorSpan = document.getElementById(`error-${fieldName}`);
            if (errorSpan) {
              const messages = errorList.map((err) => err.message).join(" ");
              errorSpan.textContent = messages;
            }

            const inputEl = form.querySelector(`[name=${fieldName}]`);
            if (inputEl) {
              inputEl.classList.add("is-invalid");
              inputEl.setAttribute("aria-invalid", "true");
              if (!firstErroneousInput) {
                firstErroneousInput = inputEl;
              }
            }
          }

          if (firstErroneousInput) {
            firstErroneousInput.focus();
          }
        }
      } else {
        throw new Error("Server error");
      }
    } catch (err) {
      console.error(err);
      clearInterval(submitInterval);
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
      
      // Display error inside modal
      if (modalErrorContainer && modalErrorText) {
        modalErrorText.textContent = "Erreur : Une erreur est survenue lors de la validation. Veuillez réessayer.";
        showStatus(modalErrorContainer);
      } else {
        alert("Erreur : Une erreur est survenue lors de la validation. Veuillez réessayer.");
      }
    }
  }

  async function executeLeadCreation(listingId) {
    const contactButtons = document.querySelectorAll("[data-contact-whatsapp]");
    const ctaErrorContainer = document.getElementById("handoff-error-cta");
    const ctaErrorText = ctaErrorContainer ? ctaErrorContainer.querySelector(".error-text") : null;
    const ctaSuccessContainer = document.getElementById("handoff-success-cta");
    const fallbackLink = document.getElementById("handoff-fallback-link");
    const modalErrorContainer = document.getElementById("handoff-error-modal");
    const modalErrorText = modalErrorContainer ? modalErrorContainer.querySelector(".error-text") : null;

    // Hide any previous messages
    hideStatus(ctaErrorContainer);
    hideStatus(ctaSuccessContainer);
    hideStatus(modalErrorContainer);

    // Keep track of original text of buttons
    const originalTexts = new Map();
    contactButtons.forEach((btn) => {
      originalTexts.set(btn, btn.textContent);
      btn.disabled = true;
    });

    // Animate button texts with dots
    let dotCount = 0;
    contactButtons.forEach((btn) => {
      btn.textContent = "Envoi en cours";
    });
    const buttonInterval = setInterval(() => {
      dotCount = (dotCount + 1) % 4;
      contactButtons.forEach((btn) => {
        btn.textContent = "Envoi en cours" + ".".repeat(dotCount);
      });
    }, 400);

    const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");
    const csrfToken = csrfInput ? csrfInput.value : getCookie("csrftoken");

    const formData = new FormData();
    formData.append(
      "acquisition_context",
      JSON.stringify({
        source: "direct_contact",
        path: window.location.pathname,
        search: window.location.search,
      })
    );

    try {
      const response = await fetch(`/listings/${listingId}/create-lead/`, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      clearInterval(buttonInterval);

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          console.log(`[WhatsApp Handoff] Lead created successfully: ${data.lead_id}`);
          if (data.whatsapp_url) {
            // Set up fallback/success state
            if (ctaSuccessContainer && fallbackLink) {
              fallbackLink.href = data.whatsapp_url;
              showStatus(ctaSuccessContainer);
              fallbackLink.focus();
            }
            
            // Redirect
            window.location.href = data.whatsapp_url;
            return true;
          } else {
            throw new Error("Le lien WhatsApp n'a pas pu être généré.");
          }
        }
      }
      
      // If we got here, it's a failure (response not ok or data.success false)
      let errorMessage = "Échec de la création du contact. Veuillez réessayer.";
      try {
        const data = await response.json();
        errorMessage = data.error || errorMessage;
      } catch (e) {}

      // Display error
      // Check if modal is currently open
      const modal = document.getElementById("identification-modal");
      const isModalOpen = modal && modal.open;

      if (isModalOpen && modalErrorContainer && modalErrorText) {
        modalErrorText.textContent = "Erreur : " + errorMessage;
        showStatus(modalErrorContainer);
      } else if (ctaErrorContainer && ctaErrorText) {
        ctaErrorText.textContent = "Erreur : " + errorMessage;
        showStatus(ctaErrorContainer);
      } else {
        alert("Erreur : " + errorMessage);
      }

      // Restore button states
      contactButtons.forEach((btn) => {
        btn.textContent = originalTexts.get(btn) || "Contacter sur WhatsApp";
        btn.disabled = false;
      });

      return false;

    } catch (err) {
      console.error(err);
      clearInterval(buttonInterval);

      const errorMessage = "Une erreur de connexion est survenue. Veuillez réessayer.";
      const modal = document.getElementById("identification-modal");
      const isModalOpen = modal && modal.open;

      if (isModalOpen && modalErrorContainer && modalErrorText) {
        modalErrorText.textContent = "Erreur : " + errorMessage;
        showStatus(modalErrorContainer);
      } else if (ctaErrorContainer && ctaErrorText) {
        ctaErrorText.textContent = "Erreur : " + errorMessage;
        showStatus(ctaErrorContainer);
      } else {
        alert("Erreur : " + errorMessage);
      }

      // Restore button states
      contactButtons.forEach((btn) => {
        btn.textContent = originalTexts.get(btn) || "Contacter sur WhatsApp";
        btn.disabled = false;
      });

      return false;
    }
  }

  async function triggerLeadCreation(button) {
    const listingId = button.dataset.listingId;
    await executeLeadCreation(listingId);
  }

  // Keyboard accessibility and focus trap for the dialog
  const modal = document.getElementById("identification-modal");
  if (modal) {
    modal.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        const focusableElements = modal.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusableElements.length === 0) return;

        const firstEl = focusableElements[0];
        const lastEl = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstEl) {
            lastEl.focus();
            e.preventDefault();
          }
        } else {
          if (document.activeElement === lastEl) {
            firstEl.focus();
            e.preventDefault();
          }
        }
      }
    });

    // Close on backdrop click
    modal.addEventListener("click", (e) => {
      const rect = modal.getBoundingClientRect();
      const isInDialog = (
        e.clientX >= rect.left &&
        e.clientX <= rect.right &&
        e.clientY >= rect.top &&
        e.clientY <= rect.bottom
      );
      if (!isInDialog) {
        closeIdentificationModal();
      }
    });
  }
});
