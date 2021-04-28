// Creating map object
var myMap = L.map("map", {
  center: [30, -5.95],
  zoom: 3
});

// Adding tile layer to the map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);

// Store API URL
var url = "http://127.0.0.1:5000/api/v1/resources/ev_charging_station/all";

// Grab the data with d3
d3.json(url, function(response) {

  // Create a new marker cluster group
  var markers = L.markerClusterGroup();

  // Loop through data
  for (var i = 0; i < response.length; i++) {
  // for (var i = 0; i < 50; i++) {

    // Set the data location property to a variable
    var location = response[i].location_name;
    console.log(location);
    // Check for location property
    if (location) {

      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([response[i].Latitude, response[i].Longitude])
        .bindPopup(response[i].location_name));
    }

  }

  // Add our marker cluster layer to the map
  myMap.addLayer(markers);

});
