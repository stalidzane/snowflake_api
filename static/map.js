console.log("map.js loaded");

// Initialize variables for selected countries
let country1 = null;
let country2 = null;

// Initialize the map
const map = L.map('map').setView([20, 0], 2);

// Set maximum bounds to limit the viewable area to the world map
var bounds = [[-100, -180], [85, 180]];
map.setMaxBounds(bounds);
map.on('drag', function() {
    map.panInsideBounds(bounds, { animate: false });
});
// Load the tile layer for the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 5,
    minZoom: 2,
    noWrap: true,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Load GeoJSON data for countries
fetch('https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            onEachFeature: function (feature, layer) {
                layer.on('click', function () {
                    if (!country1) {
                        country1 = feature.properties.ADMIN;
                        document.getElementById('country1').value = country1;
                        alert('You selected ' + country1 + '. Now choose another country.');
                        console.log(country1)
                    } else if (!country2) {
                        country2 = feature.properties.ADMIN;
                        document.getElementById('country2').value = country2;
                        alert('You selected ' + country2 + '.');
                        console.log(country2)
                    }
                });
            }
        }).addTo(map);
    });

