import json

# Read JSON data from a file
with open('countries.geojson', 'r') as file:
    parsed_data = json.load(file)

# Extract country names
country_names = [feature['properties']['ADMIN'] for feature in parsed_data['features']]

# Print the country names
with open('countries_map.txt', 'w') as file:
    for name in country_names:
         file.write(name + '\n') 
