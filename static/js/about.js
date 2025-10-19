// ===== Mobile Navbar Toggle =====
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");

hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("active");
  hamburger.classList.toggle("toggle");
});

// ===== Expand/Collapse Sections =====
const toggleSections = document.querySelectorAll(".about-section h2");
toggleSections.forEach(heading => {
  const content = heading.nextElementSibling;
  heading.style.cursor = "pointer";
  content.style.transition = "all 0.3s ease";
  content.style.overflow = "hidden";
  
  heading.addEventListener("click", () => {
    if(content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
  // Start collapsed
  content.style.maxHeight = "0px";
});

// ===== Team Member Hover Effect =====
const teamMembers = document.querySelectorAll(".team-member");
teamMembers.forEach(member => {
  member.addEventListener("mouseenter", () => {
    member.style.transform = "scale(1.05)";
    member.style.boxShadow = "0 8px 15px rgba(0,0,0,0.2)";
  });
  member.addEventListener("mouseleave", () => {
    member.style.transform = "scale(1)";
    member.style.boxShadow = "0 2px 5px rgba(0,0,0,0.1)";
  });
});

// ===== Scroll Fade-in Animation =====
const faders = document.querySelectorAll(".about-section h1, .about-section p, .about-section ul, .team-member");

const appearOptions = {
  threshold: 0.2,
  rootMargin: "0px 0px -50px 0px"
};

const appearOnScroll = new IntersectionObserver((entries, appearOnScroll) => {
  entries.forEach(entry => {
    if(!entry.isIntersecting) return;
    entry.target.classList.add("appear");
    appearOnScroll.unobserve(entry.target);
  });
}, appearOptions);

faders.forEach(fader => {
  fader.classList.add("fade"); // add fade initial class
  appearOnScroll.observe(fader);
});
