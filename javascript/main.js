window.addEventListener("DOMContentLoaded", () => {
  // Navbar shrink function
  let navbarShrink = function () {
    const navbarCollapsible = document.body.querySelector("#mainNav");
    if (!navbarCollapsible) {
      return;
    }
    if (window.scrollY === 0) {
      navbarCollapsible.classList.remove("navbar-shrink");
    } else {
      navbarCollapsible.classList.add("navbar-shrink");
    }
  };
  Particles.init({
    selector: ".particles",
    color: "#ffc800",
    connectParticles: true,
    speed: 0.2,
    responsive: [
      {
        breakpoint: 768,
        options: {
          maxParticles: 100,
        },
      },
      {
        breakpoint: 425,
        options: {
          maxParticles: 50,
        },
      },
    ],
  });

  // Shrink the navbar
  navbarShrink();

  // Shrink the navbar when page is scrolled
  document.addEventListener("scroll", navbarShrink);

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.body.querySelector("#mainNav");
  if (mainNav) {
    new bootstrap.ScrollSpy(document.body, {
      target: "#mainNav",
    });
  }

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector(".navbar-toggler");
  const responsiveNavItems = [].slice.call(
    document.querySelectorAll("#navbarResponsive .nav-link")
  );
  responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener("click", () => {
      if (window.getComputedStyle(navbarToggler).display !== "none") {
        navbarToggler.click();
      }
    });
  });

  // Send message ajax request
  const contactForm = document.getElementById("contactForm");
  if (contactForm && window.CONTACT_FORM_ENDPOINT_TRIGGER) {
    contactForm.addEventListener("submit", function (event) {
      // Stop from reloading the page
      event.preventDefault();

      // Set button spinner
      const submitButton = document.getElementById("submitButton");
      submitButton.classList.add("loading");
      submitButton.disabled = true;

      // Reset messages
      const success_message = document.getElementById("submit-success-message");
      const error_message = document.getElementById("submit-error-message");
      success_message.classList.add("d-none");
      error_message.classList.add("d-none");

      // Get email details
      const name = encodeURI(document.getElementById("contact-name").value);
      const email = encodeURI(document.getElementById("contact-email").value);
      const message = encodeURI(
        document.getElementById("contact-message").value
      );

      // Send AJAX request
      let xhr = new XMLHttpRequest();
      const url =
        window.CONTACT_FORM_ENDPOINT_TRIGGER +
        "/api/send-email?name=" +
        name +
        "&email=" +
        email +
        "&message=" +
        message;
      xhr.open("GET", url, true);
      xhr.onreadystatechange = () => {
        // In local files, status is 0 upon success in Mozilla Firefox
        if (xhr.readyState === XMLHttpRequest.DONE) {
          const response_status = xhr.status;

          if (response_status == 200) {
            success_message.classList.remove("d-none");
          } else {
            error_message.classList.remove("d-none");
          }
					// Reset button spinner
          submitButton.classList.remove("loading");
          submitButton.disabled = false;
        }
      };
      xhr.send();
    });
  }
});
