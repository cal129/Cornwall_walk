(function () {
    const mapEl = document.getElementById("walk-map");
    if (!mapEl) {
        return;
    }

    const raw = mapEl.dataset.coordinates || "";
    const matches = raw.match(/([+-]?\d+(?:\.\d+)?)[^\dA-Za-z]*([NSEW])?/gi) || [];

    let lat = null;
    let lng = null;

    if (matches.length >= 2) {
        const parsePart = (part) => {
            const valueMatch = part.match(/([+-]?\d+(?:\.\d+)?)/);
            const dirMatch = part.match(/[NSEW]/i);
            if (!valueMatch) {
                return null;
            }
            let value = parseFloat(valueMatch[1]);
            if (dirMatch) {
                const dir = dirMatch[0].toUpperCase();
                if (dir === "S" || dir === "W") {
                    value *= -1;
                }
            }
            return value;
        };

        lat = parsePart(matches[0]);
        lng = parsePart(matches[1]);
    }

    if (lat === null || lng === null || Number.isNaN(lat) || Number.isNaN(lng)) {
        mapEl.innerHTML = "<p class=\"text-muted\">Map coordinates unavailable.</p>";
        return;
    }

    const map = L.map(mapEl).setView([lat, lng], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    L.marker([lat, lng]).addTo(map);
})();
