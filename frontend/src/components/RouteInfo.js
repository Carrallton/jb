import React from 'react';

const RouteInfo = ({ route }) => {
  const transportIcons = {
    walking: '🚶',
    public: '🚌',
    mixed: '🚶+🚌'
  };

  return (
    <div className="route-info">
      <div className="route-stats">
        <div className="stat-item">
          <span className="stat-label">Distance:</span>
          <span className="stat-value">{route.distance_km} km</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Time:</span>
          <span className="stat-value">{Math.floor(route.estimated_time_min / 60)}h {route.estimated_time_min % 60}m</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Transport:</span>
          <span className="stat-value">
            {transportIcons[route.transport_type]} {route.transport_type}
          </span>
        </div>
      </div>
      
      <div className="route-categories">
        {route.categories.map(category => (
          <span key={category.id} className="category-badge">
            {category.icon && <span className="category-icon">{category.icon}</span>}
            {category.name}
          </span>
        ))}
      </div>
    </div>
  );
};

export default RouteInfo;