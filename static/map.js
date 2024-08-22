console.log("map.js loaded");
// Country names which are different in map and database and country names which are not in the database
const countryMap = {
    "American Samoa": "Samoa",
    "Bolivia": "Bolivia, Plurinational State of",
    "British Virgin Islands": "Virgin Islands, British",
    "United States Virgin Islands": "Virgin Islands, U.S.",
    "Brunei": "Brunei Darussalam",
    "Cape Verde": "Cabo Verde",
    "Czech Republic": "Czechia",
    "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
    "Republic of Congo": "Congo",
    "East Timor": "Timor-Leste",
    "Falkland Islands": "Falkland Islands (Malvinas)",
    "Guinea Bissau": "Guinea-Bissau",
    "Iran": "Iran, Islamic Republic of",
    "Laos": "Lao People's Democratic Republic",
    "Macedonia": "North Macedonia",
    "Moldova": "Moldova, Republic of",
    "South Korea": "Korea, Republic of",
    "North Korea": "Korea, Republic of",
    "Palestine": "Palestine, State of",
    "Northern Cyprus": "Cyprus",
    "Russia": "Russian Federation",
    "Republic of Serbia": "Serbia",
    "Syria": "Syrian Arab Republic",
    "Taiwan": "Taiwan, Province of China",
    "United Republic of Tanzania": "Tanzania, United Republic of",
    "Vietnam": "Viet Nam",
    "Venezuela": "Venezuela, Bolivarian Republic of",
    "United States of America": "United States",
    "United Kingdom": "United Kingdom",
    "Vatican": "Holy See (Vatican City State)",
};

const invalidMap = [
"Akrotiri Sovereign Base Area",
"Aland",
"Antarctica",
"Ashmore and Cartier Islands",
"Bajo Nuevo Bank (Petrel Is.)",
"Baykonur Cosmodrome",
"British Indian Ocean Territory",
"Clipperton Island",
"Cook Islands",
"Coral Sea Islands",
"Cyprus No Mans Area",
"Dhekelia Sovereign Base Area",
"Federated States of Micronesia",
"French Southern and Antarctic Lands",
"Heard Island and McDonald Islands",
"Hong Kong S.A.R.",
"Indian Ocean Territories",
"Ivory Coast",
"Kiribati",
"Macao S.A.R",
"Nauru",
"Niue",
"Norfolk Island",
"Palau",
"Pitcairn Islands",
"Saint Barthelemy",
"Saint Helena",
"Saint Martin",
"Saint Pierre and Miquelon",
"Scarborough Reef",
"Serranilla Bank",
"Siachen Glacier",
"Sint Maarten",
"Somaliland",
"South Georgia and South Sandwich Islands",
"Spratly Islands",
"Swaziland",
"The Bahamas",
"Tonga",
"Turkmenistan",
"Tuvalu",
"US Naval Base Guantanamo Bay",
"United Republic of Tanzania",
"United States Minor Outlying Islands"
];    
console.log("import successful")

// Function to convert country names from those in the map to the ones in the database, if they differ
function adjustCountryName(mapName) {
    if (mapName in countryMap) {
        return countryMap[mapName];
    } else if (mapName in invalidMap){
        alert(`Unfortunately, ${mapName} is not available. Please choose another country.`);
        return clearSelection();
    } else {
        return mapName
    }
};
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
                    console.log('Clicked!')
                    if (!country1) {
                        country1 = adjustCountryName(feature.properties.ADMIN)
                        document.getElementById('country1').value = country1;
                        alert('You selected ' + country1 + '. Now choose another country.');
                    } else if (!country2) {
                        country2 = adjustCountryName(feature.properties.ADMIN)
                        document.getElementById('country2').value = country2;
                        alert('You selected ' + country2 + '.');
                    }
                });
            }
        }).addTo(map);
    });

