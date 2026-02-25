document.addEventListener('DOMContentLoaded', function() {
    const walkMarkersElement = document.getElementById('walk-markers-data');
    if (!walkMarkersElement) return;
    
    const walkMarkers = JSON.parse(walkMarkersElement.textContent);
    
    if (!document.getElementById('walk-map')) return;
    
    // Initialize map centered on Cornwall
    const map = L.map('walk-map').setView([50.5, -4.8], 8);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Add markers for each walk
    walkMarkers.forEach(walk => {
        L.circleMarker([walk.lat, walk.lng], {
            radius: 8,
            fillColor: '#559ac5',
            color: '#1a1a19',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        }).bindPopup(
            `<strong>${walk.title}</strong><br>${walk.location}<br><a href="/walks/${walk.slug}/">View walk</a>`
        ).addTo(map);
    });
    
    // Fit map to bounds of markers if any exist
    if (walkMarkers.length > 0) {
        const group = new L.featureGroup(walkMarkers.map(w => L.circleMarker([w.lat, w.lng])));
        map.fitBounds(group.getBounds().pad(0.1));
    }
});
