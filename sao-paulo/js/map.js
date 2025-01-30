var hexagonIndex = {};

// Styles
var transparentStyle = new ol.style.Style({
    fill: new ol.style.Fill({
        color: [0, 0, 0, 0]
    }),
    stroke: null,
    zIndex: 3
});

var hexagonStyle = new ol.style.Style({
    fill: new ol.style.Fill({
        color: [0, 255, 0, 0.1]
    }),
    stroke: new ol.style.Stroke({
        color: [0, 100, 0, 1],
        width: 1
    }),
    zIndex: 2
});

var stationStyle = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        fill: new ol.style.Fill({
            color: [255, 255, 0, 1]
        }),
        stroke: new ol.style.Stroke({
            color: [100, 100, 0, 1],
            width: 1
        })
    }),
    zIndex: 1
});

// Popup
var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');
var overlay = new ol.Overlay({
    element: container,
    autoPan: true,
    autoPanAnimation: { duration: 250 }
});
closer.onclick = function() {
    overlay.setPosition(undefined);
    closer.blur();
    return false;
};

// Map
var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        }),
    ],
    overlays: [overlay],
    view: new ol.View({
        center: ol.proj.fromLonLat([-46.6826, -23.5858]),
        zoom: 15
    })
});

// Map click
var collection = new ol.Collection();
var featureOverlay = new ol.layer.Vector({
    map: map,
    source: new ol.source.Vector({ features: collection }),
    style: hexagonStyle,
});

map.on('click', function(browserEvent) {
    var hexagon;
    var station;
    content.innerHTML = '';
    map.forEachFeatureAtPixel(browserEvent.pixel, function(feature, layer) {
        // Add current hexagon to featureOverlay
        featureOverlay.getSource().clear();
        featureOverlay.getSource().addFeature(feature);
        // Identify elements
        if (feature.values_.stationName !== undefined)
            station = feature;
        else
            hexagon = feature;
    });
    
    if (station) {
        content.innerHTML += 'Station: <b>' + station.values_.stationName + '</b><br>';
        content.innerHTML += 'Empty slots: ' + station.values_.emptySlots + '<br>';
        content.innerHTML += 'Free bikes: ' + station.values_.freeBikes + '<br>';
        if (station.values_.usageMetric)
            content.innerHTML += 'Usage: ' + station.values_.usageMetric + '<br>';
        content.innerHTML += '<br>';
    }
    
    var socioeconomic = hexagonIndex[hexagon.values_.hex_id];
    content.innerHTML += '<i><u>Socioeconomic data:</u></i><br>';
    content.innerHTML += '<i>Population:</i> ' + socioeconomic['population'] + '<br>';
    content.innerHTML += '<i>Job quantity:</i> ' + socioeconomic['job_qty'] + '<br>';
    content.innerHTML += '<i>Health quantity:</i> ' + socioeconomic['health_qty'] + '<br>';
    content.innerHTML += '<i>Education quantity:</i> ' + socioeconomic['education_qty'] + '<br>';
    content.innerHTML += '<i>0 to 2 salaries:</i> ' + socioeconomic['0_2_salaries'] + '<br>';
    content.innerHTML += '<i>2 to 3 salaries:</i> ' + socioeconomic['2_3_salaries'] + '<br>';
    content.innerHTML += '<i>3 to 5 salaries:</i> ' + socioeconomic['3_5_salaries'] + '<br>';
    content.innerHTML += '<i>5 to 10 salaries:</i> ' + socioeconomic['5_10_salaries'] + '<br>';
    content.innerHTML += '<i>10+ salaries:</i> ' + socioeconomic['above_10_salaries'] + '<br>';
    
    overlay.setPosition(browserEvent.coordinate);
});

// Load hexagons geolocation data first
$.get('../data/scipopulis/hexagons_saopaulo_sp.json', function(data) {
    var features = new ol.format.GeoJSON({featureProjection: 'EPSG:3857'}).readFeatures(data);
    map.addLayer(new ol.layer.Vector({
        source: new ol.source.Vector({ features: features, projection: 'EPSG:3857' }),
        style: transparentStyle
    }));
    
    // Then, load hexagons socioeconomic indicators
    loadHexagonIndex();
});

function loadHexagonIndex() {
    $.get('../data/output/hexagon_index.json', function(data) {
        hexagonIndex = data;
        // Finally, load station points
        loadStations();
    });
}

function loadStations() {
    $.get('../data/output/stations.json', function(data) {
        var icons = [];
        var stations = data;
        for (var s in stations) {
            var feature = new ol.Feature({ 
                geometry: new ol.geom.Point(ol.proj.transform([stations[s].longitude, stations[s].latitude],
                                            'EPSG:4326', 'EPSG:3857')),
                stationName: stations[s].name,
                emptySlots: stations[s].empty_slots,
                freeBikes: stations[s].free_bikes,
                usageMetric: stations[s].general_daily_increase
            });
            
            style = stationStyle.clone();

            if (stations[s].general_daily_increase) {
                if (stations[s].general_daily_increase < 4)
                    style.getImage().setRadius(4);
                else
                    style.getImage().setRadius(Math.ceil(stations[s].general_daily_increase / 10));
            }
            
            feature.setStyle(style);
            icons.push(feature);
        }
        map.addLayer(new ol.layer.Vector({
            source: new ol.source.Vector({ features: icons })
        }));
        
        
    });
}
