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


# --- NON preparo più vessel_js_list per JS, sarà letto da vessels.json via JS ---

# Fit map to bounds of all markers
if all_marker_coordinates:
    min_lat = min(coord[0] for coord in all_marker_coordinates)
    max_lat = max(coord[0] for coord in all_marker_coordinates)
    min_lon = min(coord[1] for coord in all_marker_coordinates)
    max_lon = max(coord[1] for coord in all_marker_coordinates)
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
    marker_js = """
                window._map.setView([vessel.lat, vessel.lon], 18);
                setTimeout(function() {
                    if(window._markerCluster && window._markerCluster.hasLayer && window._markerCluster.hasLayer(marker)) {
                        window._markerCluster.removeLayer(marker);
                        window._map.addLayer(marker);
                        window._extractedMarkers.add(marker);
                    }
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

// --- Carica vessels.json e genera marker dinamicamente ---
function createMarkersAndFitBounds(vessels) {
    if(!window._map || !window.L) return;
    if(!window._markerCluster) {
        window._markerCluster = L.markerClusterGroup();
        window._map.addLayer(window._markerCluster);
    }
    let allCoords = [];
    vessels.forEach(function(vessel) {
        let marker = L.marker([vessel.lat, vessel.lon]);
        let popupHtml = `<div class='p-2'><h3 style='font-size:1.125rem;font-weight:bold;'>${vessel.name}</h3></div>`;
        if(vessel.last_update || vessel.status || vessel.type) {
            popupHtml += `<p style='font-size:0.875rem;color:#4B5563;'>Last update: ${vessel.last_update ? vessel.last_update.replace('T',' ').slice(0,19) : '-'}</p><div style='margin-top:0.5rem;font-size:0.875rem;'><p><span style='font-weight:600;'>Status:</span> ${vessel.status || '-'}</p><p><span style='font-weight:600;'>Type:</span> ${vessel.type || '-'}</p></div>`;
        }
        marker.bindPopup(popupHtml, {maxWidth: 300});
        window._markerCluster.addLayer(marker);
        window._vesselMarkers.set(vessel.id, marker);
        allCoords.push([vessel.lat, vessel.lon]);
        marker.on('popupclose', function() {
            if(window._extractedMarkers.has(marker)) {
                window._map.removeLayer(marker);
                window._markerCluster.addLayer(marker);
                window._extractedMarkers.delete(marker);
            }
        });
    });
    if(allCoords.length > 0) {
        window._map.fitBounds(allCoords);
    }
}

// Carica vessels.json e aggiorna vesselList, marker e tabella
fetch('vessels.json')
    .then(resp => resp.json())
    .then(json => {
        // Supporta sia formato {vessels: [...]} che lista pura
        vesselList = Array.isArray(json) ? json : (json.vessels || []);
        createMarkersAndFitBounds(vesselList);
        renderVesselTable(vesselList);
    })
    .catch(err => {
        console.error('Errore caricamento vessels.json', err);
    });
</script>

# Non serve più sostituire il placeholder vesselList

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
'''
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
