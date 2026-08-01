/** @format */

const API_URL = "http://127.0.0.1:8000/api/v1/FuelStation/";

// "GET"       -> source/destination sent as query params (?source=...&destination=...)
// "POST_FORM" -> source/destination sent as multipart/form-data (matches Postman "form-data" body)
// "POST_JSON" -> source/destination sent as a JSON body
const REQUEST_METHOD = "POST_FORM";

// The field names your API expects. Change these if your backend uses
// different names (e.g. "start"/"end", "origin"/"destination", etc.)
const SOURCE_PARAM = "source";
const DESTINATION_PARAM = "destination";

const map = L.map("map").setView([39.5, -98.35], 5); // default: continental US

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

const statusEl = document.getElementById("status");
const totalCostEl = document.getElementById("total-cost");
const haltCountEl = document.getElementById("halt-count");
const infoPanelEl = document.getElementById("info-panel");
const formEl = document.getElementById("route-form");
const submitBtn = document.getElementById("submit-btn");
const errorEl = document.getElementById("search-error");

let routeLayer = null;
let markerLayer = null;

const fuelIcon = L.divIcon({
  className: "",
  html: `<div style="
      background:#e63946;
      width:16px;height:16px;
      border-radius:50%;
      border:2px solid #fff;
      box-shadow:0 0 3px rgba(0,0,0,0.5);
    "></div>`,
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});


formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  const source = document.getElementById("source").value.trim();
  const destination = document.getElementById("destination").value.trim();
  if (!source || !destination) return;
  loadRoute(source, destination);
});


async function loadRoute(source, destination) {
  clearError();
  clearMap();
  setLoading(true);

  try {
    let res;

    if (REQUEST_METHOD === "GET") {
      const url = new URL(API_URL);
      url.searchParams.set(SOURCE_PARAM, source);
      url.searchParams.set(DESTINATION_PARAM, destination);
      res = await fetch(url);
    } else if (REQUEST_METHOD === "POST_FORM") {
      const formData = new FormData();
      formData.set(SOURCE_PARAM, source);
      formData.set(DESTINATION_PARAM, destination);
      
      res = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });
    } else {
      res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          [SOURCE_PARAM]: source,
          [DESTINATION_PARAM]: destination,
        }),
      });
    }

    if (!res.ok) {
      const bodyText = await res.text().catch(() => "");
      throw new Error(
        `API returned ${res.status}${bodyText ? " — " + bodyText.slice(0, 200) : ""}`,
      );
    }

    const data = await res.json();

    if (data.message) {
      showError(data.message);
      return;
    }
    console.log("API response:", data);
    console.log(
      "route length:",
      (data.route || []).length,
      "halts length:",
      (data.halts || []).length,
    );
    renderRoute(data);
    infoPanelEl.style.display = "block";
  } catch (err) {
    console.error("Failed to load route:", err);
    showError(
      "Failed to load route: " +
        err.message +
        " (check the browser console/network tab for details)",
    );
  } finally {
    setLoading(false);
  }
}

function renderRoute(data) {
  const routeCoords = data.route || [];
  const halts = data.halts || [];
  const totalCost = data.total_cost;


  const latLngs = routeCoords.map(([lng, lat]) => [Number(lat), Number(lng)]);

  const bounds = [];
  const markers = [];

  if (latLngs.length > 0) {
    routeLayer = L.polyline(latLngs, {
      color: "#1d4ed8",
      weight: 4,
      opacity: 0.8,
    }).addTo(map);
    bounds.push(...latLngs);

    const startMarker = L.circleMarker(latLngs[0], {
      radius: 7,
      color: "#16a34a",
      fillColor: "#16a34a",
      fillOpacity: 1,
    })
      .bindPopup("Start")
      .addTo(map);

    const endMarker = L.circleMarker(latLngs[latLngs.length - 1], {
      radius: 7,
      color: "#000",
      fillColor: "#000",
      fillOpacity: 1,
    })
      .bindPopup("End")
      .addTo(map);

    markers.push(startMarker, endMarker);
  }

  halts.forEach((halt) => {
    const lat = Number(halt.latitude);
    const lng = Number(halt.longitude);
    const marker = L.marker([lat, lng], {
      icon: fuelIcon,
    }).addTo(map);

    const popupHtml = `
      <div class="halt-popup">
        <b>${escapeHtml(halt.truckstop_name || "Fuel stop")}</b>
        ${escapeHtml(halt.address || "")}<br>
        ${escapeHtml(halt.city || "")}, ${escapeHtml(halt.state || "")}<br>
        Price: $${escapeHtml(String(halt.retail_price ?? "—"))}
      </div>
    `;
    marker.bindPopup(popupHtml);
    markers.push(marker);
    bounds.push([lat, lng]);
  });

  markerLayer = L.layerGroup(markers).addTo(map);

  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [40, 40] });
  }

  totalCostEl.textContent = `Total cost: ${
    totalCost !== undefined ? "$" + totalCost : "—"
  }`;
  haltCountEl.textContent = `Fuel stops: ${halts.length}`;
}

function clearMap() {
  if (routeLayer) {
    map.removeLayer(routeLayer);
    routeLayer = null;
  }
  if (markerLayer) {
    map.removeLayer(markerLayer);
    markerLayer = null;
  }
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? "Loading…" : "Find Route";
  statusEl.style.display = isLoading ? "block" : "none";
}

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.style.display = "block";
}

function clearError() {
  errorEl.style.display = "none";
  errorEl.textContent = "";
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
