const showNavbar = (toggleId, navId, bodyId, headerId, profileId) => {
  const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId),
    profile = document.getElementById(profileId);

  // Validate that all variables exist
  if (toggle && nav && bodypd && headerpd && profile) {
    toggle.addEventListener("click", () => {
      // show navbar
      nav.classList.toggle("show");
      // change icon
      toggle.classList.toggle("bx-x");
      // add padding to body
      // bodypd.classList.toggle("body-pd");
      // add padding to header
      headerpd.classList.toggle("body-pd");

      profile.classList.toggle("hide");
    });
  }
};

const dropdown = document.querySelectorAll(".dropmenu");

dropdown.forEach((n) =>
  n.addEventListener("click", () => {
    const menu = n.querySelectorAll(".dropdown__menu");
    const dropicon = n.querySelectorAll(".dropdown__icon");
    menu.forEach((el) => {
      el.classList.toggle("show-menu");
    });
    dropicon.forEach((el) => {
      el.classList.toggle("rotate-icon");
    });
  })
);

showNavbar("header-toggle", "nav-bar", "body-pd", "header", "profile");
