const navLinks = document.querySelectorAll('.nav-link');
const pages = document.querySelectorAll('.page');

function showPage(pageId) {
  navLinks.forEach((link) => {
    const isActive = link.dataset.page === pageId;
    link.classList.toggle('active', isActive);
  });

  pages.forEach((page) => {
    page.classList.toggle('active', page.id === pageId);
  });
}

navLinks.forEach((link) => {
  link.addEventListener('click', () => {
    showPage(link.dataset.page);
  });
});
