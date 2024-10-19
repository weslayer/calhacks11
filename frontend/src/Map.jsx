import React, { useRef, useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN;

function Map({children}) {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const markersRef = useRef({})
  const [lng, setLng] = useState(-122.4428);
  const [lat, setLat] = useState(37.75);
  const [zoom, setZoom] = useState(12);

  useEffect(() => {
    if (map.current) return; // initialize map only once
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/dark-v11',
      center: [lng, lat],
      minZoom: 11,
      pitch: 40,
      worldview: "US",
      zoom: zoom
    });

    map.current.on('move', () => {
      setLng(map.current.getCenter().lng.toFixed(4));
      setLat(map.current.getCenter().lat.toFixed(4));
      setZoom(map.current.getZoom().toFixed(2));
    });

  }, []);

  useEffect(() => {
    if (!map.current) return;

    // Remove existing markers
    Object.values(markersRef.current).forEach(marker => marker.remove());
    markersRef.current = {};

    // Add new markers
    React.Children.forEach(children, child => {
      if (child.type.name === 'Marker') {
        const { longitude, latitude, color } = child.props;
        
        // Create a custom dot marker
        const el = document.createElement('div');
        el.className = 'dot-marker';
        el.style.backgroundColor = color;
        el.style.width = '10px';
        el.style.height = '10px';
        el.style.borderRadius = '50%';

        const marker = new mapboxgl.Marker(el)
          .setLngLat([longitude, latitude])
          .addTo(map.current);
        markersRef.current[`${longitude}-${latitude}`] = marker;
      }
    });
  }, [children]);

  return (
    <div>
      <div ref={mapContainer} className="map-container" />
    </div>
  );
}

export default Map;