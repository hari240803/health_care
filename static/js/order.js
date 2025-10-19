// ===== Mobile Navbar Toggle =====
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");

hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("active");
  hamburger.classList.toggle("toggle");
});

// ===== Sample dataset: Zip -> Towns -> Landmarks =====
const zipData = {
  "500001": { towns: ["Hyderabad", "Secunderabad"], landmarks: { "Hyderabad":["Charminar","Banjara Hills"], "Secunderabad":["Cantonment","Secunderabad Club"] }},
  "110001": { towns: ["New Delhi"], landmarks: { "New Delhi":["Connaught Place","India Gate"] }},
  "600001": { towns: ["Chennai"], landmarks: { "Chennai":["Marina Beach","Parrys Corner"] }}
};

// ===== Dynamic Address Add =====
const addAddressBtn = document.getElementById("addAddressBtn");
const addressContainer = document.getElementById("addressContainer");

addAddressBtn.addEventListener("click", () => {
  const newAddress = document.createElement("div");
  newAddress.classList.add("address");
  newAddress.innerHTML = `
    <input type="text" name="fullname" placeholder="Full Name" required>
    <input type="tel" name="phone" placeholder="Phone Number" required>
    <input type="text" name="zipcode" placeholder="Enter Zip Code" class="zipcode">
    <input type="text" name="town" placeholder="Enter Town/Village" class="town" autocomplete="off" required>
    <div class="suggestions town-suggestions"></div>
    <input type="text" name="landmark" placeholder="Select Landmark" class="landmark" autocomplete="off" required>
    <div class="suggestions landmark-suggestions"></div>
    <button type="button" class="removeBtn">Remove</button>
  `;
  addressContainer.appendChild(newAddress);
  newAddress.querySelector(".removeBtn").addEventListener("click", ()=> newAddress.remove());
  initSmartAddress(newAddress);
});

// ===== Prescription Preview =====
const prescriptionInput = document.getElementById("prescription");
const previewContainer = document.getElementById("prescriptionPreview");

prescriptionInput.addEventListener("change", () => {
  previewContainer.innerHTML = "";
  const file = prescriptionInput.files[0];
  if(file){
    if(file.type.startsWith("image/")){
      const img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      img.style.maxWidth = "100%";
      img.style.borderRadius = "8px";
      previewContainer.appendChild(img);
    } else if(file.type === "application/pdf"){
      const link = document.createElement("a");
      link.href = URL.createObjectURL(file);
      link.target = "_blank";
      link.textContent = "View Prescription (PDF)";
      previewContainer.appendChild(link);
    } else {
      previewContainer.textContent = "Unsupported file type!";
    }
  }
});

// ===== Notification Logic =====
const form = document.getElementById("orderForm");
const notification = document.getElementById("successNotification");
const closeBtn = document.getElementById("closeNotification");

form.addEventListener("submit", e => {
  e.preventDefault();

  // Show notification
  notification.classList.add("show");

  // Reset form & preview
  form.reset();
  previewContainer.innerHTML = "";

  // Reset addresses to one
  addressContainer.innerHTML = `<div class="address">
    <input type="text" name="fullname" placeholder="Full Name" required>
    <input type="tel" name="phone" placeholder="Phone Number" required>
    <input type="text" name="zipcode" placeholder="Enter Zip Code" class="zipcode">
    <input type="text" name="town" placeholder="Enter Town/Village" class="town" autocomplete="off" required>
    <div class="suggestions town-suggestions"></div>
    <input type="text" name="landmark" placeholder="Select Landmark" class="landmark" autocomplete="off" required>
    <div class="suggestions landmark-suggestions"></div>
  </div>`;
  initSmartAddress(addressContainer.firstElementChild);
});

// Close notification + redirect home (Flask route)
closeBtn.addEventListener("click", ()=>{
  notification.classList.remove("show");
  setTimeout(()=>{ window.location.href = "/home"; }, 300);
});

// ===== Smart Address (Fuzzy Autocomplete + Zip Filter) =====
function initSmartAddress(addressDiv){
  const zipInput = addressDiv.querySelector(".zipcode");
  const townInput = addressDiv.querySelector(".town");
  const townSug = addressDiv.querySelector(".town-suggestions");
  const landmarkInput = addressDiv.querySelector(".landmark");
  const landmarkSug = addressDiv.querySelector(".landmark-suggestions");

  function fuzzyMatch(input, list){
    const term = input.trim().toLowerCase();
    return list.filter(item => item.toLowerCase().includes(term));
  }

  function showSuggestions(input, suggestionsDiv, list){
    suggestionsDiv.innerHTML = "";
    list.forEach(item => {
      const div = document.createElement("div");
      div.textContent = item;
      div.addEventListener("click", ()=> {
        input.value = item;
        suggestionsDiv.style.display = "none";
        if(input === townInput){ updateLandmarks(); }
      });
      suggestionsDiv.appendChild(div);
    });
    suggestionsDiv.style.display = list.length ? "block" : "none";
  }

  function updateTowns(){
    let towns = [];
    const zip = zipInput.value.trim();
    if(zipData[zip]) towns = zipData[zip].towns;
    const matches = fuzzyMatch(townInput.value, towns);
    showSuggestions(townInput, townSug, matches);
  }

  function updateLandmarks(){
    let landmarks = [];
    const zip = zipInput.value.trim();
    const town = townInput.value.trim();
    if(zipData[zip] && zipData[zip].landmarks[town]) landmarks = zipData[zip].landmarks[town];
    const matches = fuzzyMatch(landmarkInput.value, landmarks);
    showSuggestions(landmarkInput, landmarkSug, matches);
  }

  zipInput.addEventListener("input", updateTowns);
  townInput.addEventListener("input", updateTowns);
  townInput.addEventListener("focus", updateTowns);
  landmarkInput.addEventListener("input", updateLandmarks);
  landmarkInput.addEventListener("focus", updateLandmarks);

  document.addEventListener("click", (e)=>{
    if(!townSug.contains(e.target) && e.target !== townInput) townSug.style.display = "none";
    if(!landmarkSug.contains(e.target) && e.target !== landmarkInput) landmarkSug.style.display = "none";
  });
}

// Initialize first address
initSmartAddress(addressContainer.firstElementChild);
