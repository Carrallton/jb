import React, { useState } from 'react';
import axios from 'axios';

const GPXUpload = ({ routeId, onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('gpx_file', file);

    try {
      setIsUploading(true);
      const response = await axios.post(
        `/api/routes/${routeId}/upload_gpx/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      onUploadSuccess();
      setFile(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="gpx-upload">
      <h4>Import from GPX</h4>
      <input type="file" accept=".gpx" onChange={handleFileChange} />
      <button 
        onClick={handleUpload} 
        disabled={!file || isUploading}
      >
        {isUploading ? 'Uploading...' : 'Upload GPX'}
      </button>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default GPXUpload;