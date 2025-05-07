import React from 'react';

const DownloadButton = ({ route }) => {
  const handleDownload = () => {
    // Format route data for download
    const routeData = {
      title: route.title,
      description: route.description,
      points: route.points.map(point => ({
        order: point.order,
        latitude: point.latitude,
        longitude: point.longitude,
        comment: point.comment
      }))
    };

    // Create download link
    const blob = new Blob([JSON.stringify(routeData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${route.title.replace(/\s+/g, '_')}_route.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <button onClick={handleDownload} className="download-button">
      Download Route for Offline
    </button>
  );
};

export default DownloadButton;