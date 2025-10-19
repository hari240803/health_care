// Sticky Navbar
window.addEventListener('scroll', () => {
  const header = document.querySelector('header');
  header.classList.toggle('sticky', window.scrollY > 0);
});

// Smooth Scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if(target){
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Hero typing animation
const heroText = "Your Health, Our Priority";
let index = 0;
const heroHeading = document.querySelector('.hero h1');

function typeHero() {
  if(index < heroText.length){
    heroHeading.textContent += heroText.charAt(index);
    index++;
    setTimeout(typeHero, 100);
  }
}
typeHero();

// Fade-in sections on scroll
const sections = document.querySelectorAll('.feature');
const observerOptions = { threshold: 0.2, rootMargin: "0px 0px -50px 0px" };

const observer = new IntersectionObserver((entries, obs) => {
  entries.forEach(entry => {
    if(entry.isIntersecting){
      entry.target.classList.add('appear');
      obs.unobserve(entry.target);
    }
  });
}, observerOptions);

sections.forEach(sec => observer.observe(sec));
