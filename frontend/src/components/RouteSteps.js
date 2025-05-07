import React from 'react';

const RouteSteps = ({ points }) => {
  return (
    <div className="route-steps">
      <h3>Route Steps</h3>
      <ol>
        {points.map((point, index) => (
          <li key={index}>
            <strong>Point {index + 1}</strong>
            <p>Coordinates: {point.latitude}, {point.longitude}</p>
            {point.comment && <p>Comment: {point.comment}</p>}
          </li>
        ))}
      </ol>
    </div>
  );
};

export default RouteSteps;