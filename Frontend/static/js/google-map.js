function init(){
    var coord = {lat: -41.1076917, lng: -71.3957839};
    var map = new google.maps.Map(document.getElementById('map'),{
      zoom: 10,
      center: coord
    });

    var iconSize = new google.maps.Size(48, 48); // Tamaño deseado del icono en píxeles
    var iconAnchor = new google.maps.Point(24, 48); // Punto de anclaje del icono (la mitad del ancho, la altura total)
    var marker = new google.maps.Marker({
      position: coord,
      map: map,
      icon: {
        url: 'static/images/GoogleMaps_Pin/Red_Marker.png',
        scaledSize: iconSize,
        anchor: iconAnchor
      }
    });
}
