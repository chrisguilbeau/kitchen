function initialize() {
    var mapOptions = {
        zoom: 10,
        center: new google.maps.LatLng(30.378950, -97.737211)
    };
    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    var trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);
    refreshClock();
}

function refreshClock(){
    $('.clock').html(moment().format(
        // 'MMMM Do YYYY, h:mm a'
        // 'dddd MMMM Do YYYY, h:mm a'
        'dddd h:mm a'
        ));
    setTimeout(refreshClock, 1000);
}

window.onload = initialize;
