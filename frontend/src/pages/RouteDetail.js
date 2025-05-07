import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import RouteMap from '../components/RouteMap';
import RouteSteps from '../components/RouteSteps';
import DownloadButton from '../components/DownloadButton';
import RouteInfo from '../components/RouteInfo';
import GPXUpload from '../components/GPXUpload';
import axios from 'axios';

const RouteDetail = () => {
  const { slug } = useParams();
  const [route, setRoute] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRoute = async () => {
      try {
        const response = await axios.get(`/api/routes/${slug}/`);
        setRoute(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRoute();
  }, [slug]);

  const handleGPXUploadSuccess = async () => {
    // Refresh route data after successful GPX upload
    const response = await axios.get(`/api/routes/${slug}/`);
    setRoute(response.data);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!route) return <div>Route not found</div>;

  return (
    <div className="route-detail">
      {route.main_image_url && (
        <div className="route-header-image">
          <img src={route.main_image_url} alt={route.title} />
        </div>
      )}
      
      <h1>{route.title}</h1>
      <p>{route.description}</p>
      
      <RouteInfo route={route} />
      
      <div className="route-map-container">
        <RouteMap points={route.points} transportType={route.transport_type} />
      </div>
      
      <div className="route-actions">
        <DownloadButton route={route} />
        {route.gpx_download_url && (
          <a 
            href={route.gpx_download_url} 
            className="btn btn-secondary"
            download
          >
            Download GPX
          </a>
        )}
        <GPXUpload 
          routeId={route.id} 
          onUploadSuccess={handleGPXUploadSuccess}
        />
      </div>
      
      <RouteSteps points={route.points} />
    </div>
  );
};

export default RouteDetail;