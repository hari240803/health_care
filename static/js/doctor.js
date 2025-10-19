// ===== Hamburger Toggle =====
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");

hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("active");
  hamburger.classList.toggle("toggle");
});

// ===== Sticky Header =====
window.addEventListener("scroll", () => {
  const header = document.querySelector("header");
  header.classList.toggle("sticky", window.scrollY > 0);
});

// ===== Multi-Step Form =====
const steps = document.querySelectorAll(".form-step");
const nextBtns = document.querySelectorAll(".next-btn");
const prevBtns = document.querySelectorAll(".prev-btn");
let currentStep = 0;

nextBtns.forEach(btn => btn.addEventListener("click", () => {
  if (!validateStep(steps[currentStep])) return;
  steps[currentStep].classList.remove("active");
  currentStep++;
  steps[currentStep].classList.add("active");
}));

prevBtns.forEach(btn => btn.addEventListener("click", () => {
  steps[currentStep].classList.remove("active");
  currentStep--;
  steps[currentStep].classList.add("active");
}));

function validateStep(step) {
  const inputs = step.querySelectorAll("input, select, textarea");
  for (let input of inputs) {
    if (!input.checkValidity()) {
      input.reportValidity();
      return false;
    }
  }
  return true;
}

// ===== Form Submission & Notification =====
const form = document.getElementById("consultForm");
const notification = document.getElementById("successNotification");
const closeBtn = document.getElementById("closeNotification");

form.addEventListener("submit", e => {
  e.preventDefault();
  notification.classList.add("show");
  steps.forEach(step => step.classList.remove("active"));
  steps[0].classList.add("active");
  currentStep = 0;
  form.reset();
});

closeBtn.addEventListener("click", () => {
  notification.classList.remove("show");
  setTimeout(() => {
    window.location.href = "/home"; // redirect after closing notification
  }, 300);
});
