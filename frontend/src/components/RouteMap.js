import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icons
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIconShadow from 'leaflet/dist/images/marker-shadow.png';

const RouteMap = ({ points, transportType }) => {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const polylineRef = useRef(null);
  const markersRef = useRef([]);
  
  // Custom icons based on transport type
  const getTransportIcon = (type) => {
    const iconUrl = type === 'public' 
      ? '/icons/bus-icon.png' 
      : '/icons/walking-icon.png';
    
    return L.icon({
      iconUrl,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowUrl: markerIconShadow,
      shadowSize: [41, 41]
    });
  };

  useEffect(() => {
    if (!mapInstance.current && points.length > 0) {
      // Initialize map
      mapInstance.current = L.map(mapRef.current).setView(
        [points[0].latitude, points[0].longitude],
        13
      );

      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(mapInstance.current);

      // Add points and polyline
      const latLngs = points.map(point => [point.latitude, point.longitude]);
      const lineColor = transportType === 'public' ? 'red' : 
                       transportType === 'mixed' ? 'purple' : 'blue';
      
      polylineRef.current = L.polyline(latLngs, { 
        color: lineColor,
        weight: 5,
        opacity: 0.7
      }).addTo(mapInstance.current);

      // Clear previous markers
      markersRef.current.forEach(marker => marker.remove());
      markersRef.current = [];

      // Add markers with custom icons
      points.forEach((point, index) => {
        const marker = L.marker([point.latitude, point.longitude], {
          icon: getTransportIcon(transportType)
        })
          .addTo(mapInstance.current)
          .bindPopup(`
            <b>Point ${index + 1}</b><br>
            ${point.comment || ''}
            ${point.image_url ? `<br><img src="${point.image_url}" style="max-width: 200px; max-height: 150px;">` : ''}
          `);
        
        markersRef.current.push(marker);
      });

      // Fit bounds to route
      mapInstance.current.fitBounds(polylineRef.current.getBounds());
    }

    return () => {
      if (mapInstance.current) {
        mapInstance.current.remove();
        mapInstance.current = null;
      }
    };
  }, [points, transportType]);

  return <div ref={mapRef} style={{ height: '500px', width: '100%' }} />;
};

export default RouteMap;