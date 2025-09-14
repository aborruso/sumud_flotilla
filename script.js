const map = L.map('map');

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function updateURL() {
    const zoom = map.getZoom();
    const center = map.getCenter();
    window.location.hash = `${zoom}/${center.lat.toFixed(4)}/${center.lng.toFixed(4)}`;
}

map.on('moveend', updateURL);
map.on('zoomend', updateURL);

fetch('vessels.json')
    .then(response => response.json())
    .then(data => {
        const markers = L.markerClusterGroup();
        const markerCoords = [];
        data.vessels.forEach(vessel => {
            if (vessel.positions && vessel.positions.length > 0) {
                const lastPosition = vessel.positions[vessel.positions.length - 1];
                const lat = lastPosition.latitude;
                const lon = lastPosition.longitude;
                const marker = L.marker([lat, lon]);
                const popupContent = `
                    <div class="p-2">
                        <h3 class="text-lg font-bold">${vessel.name}</h3>
                        <p class="text-sm text-gray-600">Last update: ${new Date(lastPosition.timestamp_utc).toLocaleString()}</p>
                        <div class="mt-2 text-sm">
                            <p><span class="font-semibold">Status:</span> ${vessel.vessel_status}</p>
                            <p><span class="font-semibold">Type:</span> ${vessel.type}</p>
                        </div>
                    </div>
                `;
                marker.bindPopup(popupContent);
                markers.addLayer(marker);
                markerCoords.push([lat, lon]);
            }
        });

        map.addLayer(markers);

        const zoomToFitButton = L.Control.extend({
            onAdd: function(map) {
                const button = L.DomUtil.create('button', 'bg-white text-black p-2 rounded-md shadow-md');
                button.innerHTML = 'Zoom to Fit';
                button.onclick = function(){
                    if (markerCoords.length > 0) {
                        map.fitBounds(markerCoords);
                    }
                }
                return button;
            }
        });
        new zoomToFitButton({ position: 'topright' }).addTo(map);

        const hash = window.location.hash;
        if (hash) {
            const parts = hash.substring(1).split('/');
            if (parts.length === 3) {
                const zoom = parseInt(parts[0], 10);
                const lat = parseFloat(parts[1]);
                const lon = parseFloat(parts[2]);
                map.setView([lat, lon], zoom);
            }
        } else if (markerCoords.length > 0) {
            map.fitBounds(markerCoords);
        } else {
            map.setView([30, 0], 2);
        }
    });