(async function() {
    const weatherWidget = document.getElementById('weather-widget');
    if (!weatherWidget) return;
    
    const coordsStr = weatherWidget.dataset.coordinates || '';
    
    const matches = coordsStr.match(/([+-]?\d+(?:\.\d+)?)[^\dA-Za-z]*([NSEW])?/gi) || [];
    if (matches.length < 2) {
        weatherWidget.innerHTML = '<p class="text-muted text-center">Weather unavailable</p>';
        return;
    }

    const parsePart = (part) => {
        const valueMatch = part.match(/([+-]?\d+(?:\.\d+)?)/);
        const dirMatch = part.match(/[NSEW]/i);
        if (!valueMatch) return null;
        let value = parseFloat(valueMatch[1]);
        if (dirMatch) {
            const dir = dirMatch[0].toUpperCase();
            if (dir === "S" || dir === "W") value *= -1;
        }
        return value;
    };

    const lat = parsePart(matches[0]);
    const lon = parsePart(matches[1]);

    if (!lat || !lon) {
        weatherWidget.innerHTML = '<p class="text-muted text-center">Weather unavailable</p>';
        return;
    }

    try {
        const response = await fetch(
            `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=auto`
        );
        const data = await response.json();

        const temp = Math.round(data.current.temperature_2m);
        const humidity = data.current.relative_humidity_2m;
        const windSpeed = Math.round(data.current.wind_speed_10m);
        const weatherCode = data.current.weather_code;

        const getWeatherIcon = (code) => {
            if (code === 0) return '☀️';
            if (code <= 3) return '🌤️';
            if (code <= 48) return '☁️';
            if (code <= 67) return '🌧️';
            if (code <= 77) return '🌨️';
            if (code <= 82) return '🌧️';
            return '⛈️';
        };

        const getWeatherDescription = (code) => {
            if (code === 0) return 'Clear sky';
            if (code <= 3) return 'Partly cloudy';
            if (code <= 48) return 'Cloudy';
            if (code <= 67) return 'Rainy';
            if (code <= 77) return 'Snowy';
            if (code <= 82) return 'Rain showers';
            return 'Thunderstorm';
        };

        weatherWidget.innerHTML = `
            <div class="weather-info">
                <div class="weather-icon">${getWeatherIcon(weatherCode)}</div>
                <div class="weather-temp">${temp}°C</div>
                <div class="weather-description">${getWeatherDescription(weatherCode)}</div>
                <div class="weather-details">
                    <div class="weather-detail-item">
                        <span class="weather-detail-label">Humidity</span>
                        <span class="weather-detail-value">${humidity}%</span>
                    </div>
                    <div class="weather-detail-item">
                        <span class="weather-detail-label">Wind</span>
                        <span class="weather-detail-value">${windSpeed} km/h</span>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        weatherWidget.innerHTML = '<p class="text-muted text-center">Weather data unavailable</p>';
    }
})();
