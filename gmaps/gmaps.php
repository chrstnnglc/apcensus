		 <!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
</head>
<body>

<h1>Google Map</h1>

	<div id="googleMap" style="width:100%;height:500px;"></div>

</body>

<script>
function myMap() {

	//set map properties
	var mapProp= {
		center: new google.maps.LatLng(14.676208,121.043861),
		zoom:18,
	};
	
	/*
	//initiate map
	var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
	
	//map marker	label: add label in marker,
	var static_marker = new google.maps.Marker({
		position: new google.maps.LatLng(14.676208,121.043861),
		label: "AP",
		map: map,
	});
	
	var marker2 = new google.maps.Marker({
		position: new google.maps.LatLng(14.676908,121.043861),
		map: map,
	});	
	var marker1 = new google.maps.Marker({
		position: new google.maps.LatLng(14.676208,121.044861),
		map: map,
	}); */
}

function initMap(){
	var mapProp= {
		center: new google.maps.LatLng(14.676208,121.043861),
		zoom:18,
	};
	var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
	var infoWindow = new google.maps.InfoWindow;
	
	var static_marker = new google.maps.Marker({
		position: new google.maps.LatLng(14.676208,121.043861),
		label: "AP",
		map: map,
	});
	
	downloadUrl('gmaps_php.php', function(data) {
		var xml = data.responseXML;
		var ap_list = xml.documentElement.getElementsByTagName('ap_list');
		Array.prototype.forEach.call(ap_list, function(ap){
			var id = ap.getAttribute('id');
			var mac = ap.getAttribute('mac');
			var ssid = ap.getAttribute('ssid');
			var isp = ap.getAttribute('isp');
			var point = new google.maps.LatLng(
				parseFloat(ap.getAttribute('lat')),
				parseFloat(ap.getAttribute('lng'))
			);
			
			var infowincontent = document.createElement('div');
			var strong = document.createElement('strong');
			strong.textContent = ssid
			infowincontent.appendChild(strong);
			infowincontent.appendChild(document.createElement('br'));
			
			var list = document.createElement('ul');
			var mac_text = document.createElement("li");
			mac_text.appendChild(document.createTextNode("MAC: "+ mac));
			ul.appendChild(mac_text);
			var ssid_text = document.createElement("li");
			ssid_text.appendChild(document.createTextNode("SSID: "+ ssid));
			ul.appendChild(ssid_text);
			var isp_text = document.createElement("li");
			isp_text.appendChild(document.createTextNode("ISP: "+ isp));
			ul.appendChild(isp_text);
			
			infowincontent.appendChild(list);
			
			var ap = new google.maps.Marker({
				map: map,
				position: point,
				label: "AP",
			});
			
			ap.addListener('hover', function() {
				infoWindow.setContent(infowincontent);
				infoWindow.open(map, ap);
			});

		});
	});
}
function downloadUrl(url,callback) {
	var request = window.ActiveXObject ?
		new ActiveXObject('Microsoft.XMLHTTP') :
		new XMLHttpRequest;

	request.onreadystatechange = function() {
		if (request.readyState == 4) {
			request.onreadystatechange = doNothing;
			callback(request, request.status);
		}
	};

	request.open('GET', url, true);
	request.send(null);
}
/*
function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: new google.maps.LatLng(14.676208,121.043861),
          zoom: 16
        });
        var infoWindow = new google.maps.InfoWindow;

          // Change this depending on the name of your PHP or XML file
          downloadUrl('gmaps_php.php', function(data) {
            var xml = data.responseXML;
            var markers = xml.documentElement.getElementsByTagName('ap_list');
            Array.prototype.forEach.call(markers, function(markerElem) {
              var id = markerElem.getAttribute('id');
              var mac = markerElem.getAttribute('mac');
              var ssid = markerElem.getAttribute('ssid');
              var isp = markerElem.getAttribute('isp');
              var point = new google.maps.LatLng(
                  parseFloat(markerElem.getAttribute('lat')),
                  parseFloat(markerElem.getAttribute('lng')));

              var infowincontent = document.createElement('div');
              var strong = document.createElement('strong');
              strong.textContent = ssid
              infowincontent.appendChild(strong);
              infowincontent.appendChild(document.createElement('br'));

              var text = document.createElement('text');
              text.textContent = isp
              infowincontent.appendChild(text);
              
              var marker = new google.maps.Marker({
                map: map,
                position: point,
                label: "AP"
              });
              marker.addListener('click', function() {
                infoWindow.setContent(infowincontent);
                infoWindow.open(map, marker);
              });
            });
          });
        }

      function downloadUrl(url, callback) {
        var request = window.ActiveXObject ?
            new ActiveXObject('Microsoft.XMLHTTP') :
            new XMLHttpRequest;

        request.onreadystatechange = function() {
          if (request.readyState == 4) {
            request.onreadystatechange = doNothing;
            callback(request, request.status);
          }
        };

        request.open('GET', url, true);
        request.send(null);
      }

      function doNothing() {}*/
function doNothing() {}
</script>

<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCz_xDT4_D32UQ__xr91UT-_P9a7bcOG2Q&callback=initMap"></script>

</html> 