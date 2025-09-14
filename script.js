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

// Modal elements
const closeModalBtn = document.getElementById('closeModalBtn');
const vesselModal = document.getElementById('vesselModal');
const vesselSearchInput = document.getElementById('vesselSearchInput');
const vesselTableBody = document.getElementById('vesselTableBody');

let allVesselsData = []; // To store all vessel data for filtering
const vesselMarkersMap = new Map(); // To store L.Marker objects keyed by vessel ID

// Close modal
closeModalBtn.addEventListener('click', () => {
    vesselModal.classList.add('hidden');
});

// Close modal when clicking outside
vesselModal.addEventListener('click', (e) => {
    if (e.target === vesselModal) {
        vesselModal.classList.add('hidden');
    }
});

// Render vessel table
function renderVesselTable(vesselsToRender) {
    vesselTableBody.innerHTML = ''; // Clear existing rows

    // Sort vessels alphabetically by name
    vesselsToRender.sort((a, b) => a.name.localeCompare(b.name));

    vesselsToRender.forEach(vessel => {
        const row = document.createElement('tr');
        row.classList.add('hover:bg-gray-100', 'cursor-pointer');
        row.innerHTML = `<td class="py-2 px-4 border-b border-gray-200">${vessel.name}</td>`;
        row.addEventListener('click', () => {
            // Navigate map to vessel position and open popup
            if (vessel.positions && vessel.positions.length > 0) {
                const lastPosition = vessel.positions[vessel.positions.length - 1];
                map.setView([lastPosition.latitude, lastPosition.longitude], 18); // Zoom to vessel
                vesselModal.classList.add('hidden'); // Close modal

                // Open popup for the corresponding marker
                const marker = vesselMarkersMap.get(vessel.id); // Assuming vessel.id is unique
                if (marker) {
                    marker.openPopup();
                }
            }
        });
        vesselTableBody.appendChild(row);
    });
}

// Search functionality
vesselSearchInput.addEventListener('keyup', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const filteredVessels = allVesselsData.filter(vessel =>
        vessel.name.toLowerCase().includes(searchTerm)
    );
    renderVesselTable(filteredVessels);
});

fetch('vessels.json')
    .then(response => response.json())
    .then(data => {
        allVesselsData = data.vessels; // Store all vessel data
        renderVesselTable(allVesselsData); // Initial render of the table

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
                        <p class="text-sm text-gray-600">Last update: ${new Date(lastPosition.timestamp_utc).toISOString().replace('T', ' ').substring(0, 19)}</p>
                        <div class="mt-2 text-sm">
                            <p><span class="font-semibold">Status:</span> ${vessel.vessel_status}</p>
                            <p><span class="font-semibold">Type:</span> ${vessel.type}</p>
                        </div>
                    </div>
                `;
                marker.bindPopup(popupContent);
                markers.addLayer(marker);
                vesselMarkersMap.set(vessel.id, marker); // Store marker in the map
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

        const openVesselListButton = L.Control.extend({
            onAdd: function(map) {
                const button = L.DomUtil.create('button', 'bg-white text-black p-2 rounded-md shadow-md');
                button.innerHTML = 'Vessel List';
                button.onclick = function() {
                    vesselModal.classList.remove('hidden');
                    renderVesselTable(allVesselsData);
                }
                return button;
            }
        });
        new openVesselListButton({ position: 'topright' }).addTo(map);

        const sourceLink = L.Control.extend({
            onAdd: function(map) {
                const link = L.DomUtil.create('a', 'bg-white text-black p-2 rounded-md shadow-md cursor-pointer');
                link.href = 'https://globalsumudflotilla.org/tracker/';
                link.innerHTML = 'Source';
                link.target = '_blank';
                return link;
            }
        });
        new sourceLink({ position: 'bottomleft' }).addTo(map);

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
        }
    });

// Fetch last updated timestamp
fetch('last_updated.txt')
    .then(response => response.text())
    .then(timestamp => {
        const sourceLinkControl = L.Control.extend({
            onAdd: function(map) {
                const link = L.DomUtil.create('a', 'bg-white text-black p-2 rounded-md shadow-md cursor-pointer');
                link.href = 'https://globalsumudflotilla.org/tracker/';
                link.innerHTML = `Source (Last updated: ${timestamp})`;
                link.target = '_blank';
                return link;
            }
        });
        new sourceLinkControl({ position: 'bottomleft' }).addTo(map);
    })
    .catch(error => {
        console.error('Error fetching last_updated.txt:', error);
        // Fallback to original source link if fetching fails
        const sourceLinkControl = L.Control.extend({
            onAdd: function(map) {
                const link = L.DomUtil.create('a', 'bg-white text-black p-2 rounded-md shadow-md cursor-pointer');
                link.href = 'https://globalsumudflotilla.org/tracker/';
                link.innerHTML = 'Source';
                link.target = '_blank';
                return link;
            }
        });
        new sourceLinkControl({ position: 'bottomleft' }).addTo(map);
    });