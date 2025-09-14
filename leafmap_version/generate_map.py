import folium
from folium.plugins import MarkerCluster, MiniMap, MeasureControl
from branca.element import MacroElement, Template
import requests
import json as pyjson

# Fetch vessel data
url = "https://flotilla-orpin.vercel.app/api/vessels"
response = requests.get(url)
data = response.json()

# List to store all marker coordinates for fitting bounds
all_marker_coordinates = []

# Create a base map (centered arbitrarily, will be reset by fit_bounds)
m = folium.Map(location=[0, 0], zoom_start=2)

# Crea il cluster
marker_cluster = MarkerCluster().add_to(m)

# Aggiungi MiniMap
MiniMap().add_to(m)

# Aggiungi MeasureControl
MeasureControl().add_to(m)

# --- Preparo lista vessel per JS ---
vessel_js_list = []
marker_refs = []
for vessel_data in data["vessels"]:
    if vessel_data["positions"] and len(vessel_data["positions"]) > 0:
        last_position = vessel_data["positions"][-1]
        lat = last_position["latitude"]
        lon = last_position["longitude"]
        name = vessel_data["name"]
        vessel_id = vessel_data.get("id", "")
        # Recupero dettagli aggiuntivi
        last_update = last_position.get("timestamp_utc", "-")
        vessel_status = vessel_data.get("vessel_status", "-")
        vessel_type = vessel_data.get("type", "-")
        popup_html = f'''
            <div class="p-2">
                <h3 style="font-size:1.125rem;font-weight:bold;">{name}</h3>
                <p style="font-size:0.875rem;color:#4B5563;">Last update: {last_update.replace('T', ' ')[:19]}</p>
                <div style="margin-top:0.5rem;font-size:0.875rem;">
                    <p><span style="font-weight:600;">Status:</span> {vessel_status}</p>
                    <p><span style="font-weight:600;">Type:</span> {vessel_type}</p>
                </div>
            </div>
        '''
        marker = folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300)
        )
        marker.add_to(marker_cluster)
        all_marker_coordinates.append([lat, lon])
        # Per JS
        marker_refs.append((vessel_id, marker))
        vessel_js_list.append({
            "id": vessel_id,
            "name": name,
            "lat": lat,
            "lon": lon
        })

# Fit map to bounds of all markers
if all_marker_coordinates:
    min_lat = min(coord[0] for coord in all_marker_coordinates)
    max_lat = max(coord[0] for coord in all_marker_coordinates)
    min_lon = min(coord[1] for coord in all_marker_coordinates)
    max_lon = max(coord[1] for coord in all_marker_coordinates)
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
    print(f"DEBUG - bounds calcolati: {bounds}")
    m.fit_bounds(bounds)

# Nota Source in basso a sinistra
with open("../last_updated.txt") as f:
        last_update = f.read().strip()

source_html = f'''
        <style>
                @media (max-width: 768px) {{
                        .source-box {{
                                display: none !important;
                        }}
                }}
        </style>
        <div class="source-box" style="position: absolute; bottom: 20px; left: 20px; z-index: 9999; background: white; color: black; padding: 5px 8px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); font-size: 11px;">
                <a href="https://globalsumudflotilla.org/tracker/" target="_blank" style="font-weight: bold; color: #1976D2; text-decoration: underline;">Source</a>
                <span style="margin-left: 8px;">(data map update: {last_update})</span>
        </div>
'''

class SourceBox(MacroElement):
        def __init__(self, html):
                super().__init__()
                self._template = Template(f"""
                        {{% macro html(this, kwargs) %}}
                        {html}
                        {{% endmacro %}}
                """)

m.get_root().add_child(SourceBox(source_html))

# --- Modale e JS per vessel list ---
modal_html = '''
<div id="vesselModal" style="display:none;position:fixed;z-index:99999;top:0;left:0;width:100vw;height:100vh;background:rgba(31,41,55,0.75);align-items:center;justify-content:center;">
    <div style="background:white;padding:2rem;border-radius:1rem;max-width:400px;width:90vw;max-height:80vh;overflow-y:auto;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
            <h2 style="font-size:1.25rem;font-weight:bold;">Vessels List</h2>
            <button id="closeModalBtn" style="font-size:2rem;line-height:1;color:#374151;background:none;border:none;cursor:pointer;">&times;</button>
        </div>
        <input id="vesselSearchInput" type="text" placeholder="Search vessels..." style="width:100%;padding:0.5rem;margin-bottom:1rem;border:1px solid #d1d5db;border-radius:0.375rem;">
        <div style="max-height:50vh;overflow-y:auto;">
            <table style="width:100%;background:white;">
                <thead><tr><th style="padding:0.5rem 1rem;border-bottom:1px solid #e5e7eb;text-align:left;font-size:0.9rem;color:#6b7280;">Vessel Name</th></tr></thead>
                <tbody id="vesselTableBody"></tbody>
            </table>
        </div>
    </div>
</div>
<button id="openVesselListBtn" style="position:absolute;top:120px;left:10px;z-index:9999;background:white;color:black;padding:0.5rem 1rem;border:2px solid rgba(0,0,0,0.2);border-radius:0.25rem;box-shadow:none;font-weight:bold;cursor:pointer;">Vessels List</button>
<button id="zoomToFitBtn" style="position:absolute;top:80px;left:10px;z-index:9999;background:white;color:black;padding:0.5rem 1rem;border:2px solid rgba(0,0,0,0.2);border-radius:0.25rem;box-shadow:none;font-weight:bold;cursor:pointer;">Zoom to fit</button>
<script>
const vesselList = __VESSEL_LIST_JSON__;
const vesselModal = document.getElementById('vesselModal');
const openVesselListBtn = document.getElementById('openVesselListBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const vesselSearchInput = document.getElementById('vesselSearchInput');
const vesselTableBody = document.getElementById('vesselTableBody');
const zoomToFitBtn = document.getElementById('zoomToFitBtn');

openVesselListBtn.onclick = function() { vesselModal.style.display = 'flex'; renderVesselTable(vesselList); };
closeModalBtn.onclick = function() { vesselModal.style.display = 'none'; };
vesselModal.onclick = function(e) { if(e.target === vesselModal) vesselModal.style.display = 'none'; };
zoomToFitBtn.onclick = function() {
    if(window._map && vesselList.length > 0) {
        var bounds = [];
        vesselList.forEach(function(vessel) {
            bounds.push([vessel.lat, vessel.lon]);
        });
        window._map.fitBounds(bounds);
    }
};

function renderVesselTable(vessels) {
    vesselTableBody.innerHTML = '';
    vessels.slice().sort(function(a,b){return a.name.localeCompare(b.name)}).forEach(function(vessel) {
        var row = document.createElement('tr');
        row.style.cursor = 'pointer';
        row.innerHTML = '<td style="padding:0.5rem 1rem;border-bottom:1px solid #e5e7eb;">' + vessel.name + '</td>';
        row.onclick = function() {
            vesselModal.style.display = 'none';
            // Usa la Map per trovare il marker
            var marker = window._vesselMarkers.get(vessel.id);
            if(marker) {
                // Prima zooma
                window._map.setView([vessel.lat, vessel.lon], 18);

                // Aspetta che il zoom sia completato, poi apri il popup
                setTimeout(function() {
                    // Se il marker è in un cluster, sclusterizza definitivamente
                    if(window._markerCluster && window._markerCluster.hasLayer && window._markerCluster.hasLayer(marker)) {
                        window._markerCluster.removeLayer(marker);
                        window._map.addLayer(marker);
                        // Traccia che questo marker è stato estratto
                        window._extractedMarkers.add(marker);
                    }

                    // Apri il popup e lascialo aperto
                    marker.openPopup();
                }, 500);
            }
        };
        vesselTableBody.appendChild(row);
    });
}
vesselSearchInput.onkeyup = function(e) {
    var term = e.target.value.toLowerCase();
    renderVesselTable(vesselList.filter(function(v){return v.name.toLowerCase().includes(term);}));
};
</script>
'''

# Sostituisco il placeholder con il JSON vero
modal_html = modal_html.replace("__VESSEL_LIST_JSON__", pyjson.dumps(vessel_js_list))

# --- JS per referenziare marker e mappa ---
marker_js = """
<script>
window._vesselMarkers = new Map();
window._map = null;
window._markerCluster = null;
window._extractedMarkers = new Set(); // Tiene traccia dei marker estratti dal cluster

// Funzione per aggiornare l'URL con posizione e zoom correnti
function updateURL() {
    if(window._map) {
        const zoom = window._map.getZoom();
        const center = window._map.getCenter();
        window.location.hash = zoom + '/' + center.lat.toFixed(4) + '/' + center.lng.toFixed(4);
    }
}

// Funzione per inizializzare riferimenti mappa
function initializeMapReferences() {
    if(window._map === null && window.L && window.L.Map && window.L.Map.prototype) {
        for (let k in window) {
            if(window[k] && window[k] instanceof window.L.Map) {
                window._map = window[k];

                // Aggiungi listeners per aggiornare URL quando mappa si sposta o zooma
                window._map.on('moveend', updateURL);
                window._map.on('zoomend', updateURL);

                // Leggi hash dall'URL per impostare vista iniziale
                const hash = window.location.hash;
                        if (hash) {
                            const parts = hash.substring(1).split('/');
                            if (parts.length === 3) {
                                const zoom = parseInt(parts[0], 10);
                                const lat = parseFloat(parts[1]);
                                const lon = parseFloat(parts[2]);
                                if (!isNaN(zoom) && !isNaN(lat) && !isNaN(lon)) {
                                    window._map.setView([lat, lon], zoom);
                                    return; // Exit early, don't trigger fit bounds
                                }
                            }
                        }

                        // Se non c'è hash valido, usa fit bounds come prima
                        // Questo sarà gestito dal comportamento predefinito di folium                // Trova il marker cluster e memorizza i marker
                window._map.eachLayer(function(layer) {
                    if(layer instanceof window.L.MarkerClusterGroup) {
                        window._markerCluster = layer;

                        // Memorizza tutti i marker con coordinate come chiave
                        layer.eachLayer(function(marker) {
                            if(marker instanceof window.L.Marker) {
                                const latLng = marker.getLatLng();
                                const coordKey = latLng.lat.toFixed(6) + "," + latLng.lng.toFixed(6);

                                // Trova l'ID vessel corrispondente
                                vesselList.forEach(function(vessel) {
                                    const vesselCoordKey = vessel.lat.toFixed(6) + "," + vessel.lon.toFixed(6);
                                    if(coordKey === vesselCoordKey) {
                                        window._vesselMarkers.set(vessel.id, marker);
                                    }
                                });

                                // Aggiungi listener per quando il popup viene chiuso
                                marker.on('popupclose', function() {
                                    // Se questo marker è stato estratto dal cluster, rimettilo
                                    if(window._extractedMarkers.has(marker)) {
                                        window._map.removeLayer(marker);
                                        window._markerCluster.addLayer(marker);
                                        window._extractedMarkers.delete(marker);
                                    }
                                });
                            }
                        });
                    }
                });
                break;
            }
        }
    }
}

// Prova a inizializzare dopo che la mappa è caricata
setTimeout(initializeMapReferences, 1000);
setTimeout(initializeMapReferences, 2000);
setTimeout(initializeMapReferences, 3000);
</script>
"""

m.get_root().html.add_child(folium.Element(marker_js + modal_html))

# Save the map as an HTML file
output_html = "../index.html"
m.save(output_html)
print(f"Map saved to {output_html}")
