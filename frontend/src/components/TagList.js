import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TagList() {
  const [tags, setTags] = useState([]);

  useEffect(() => {
    fetchTags();
  }, []);

  const fetchTags = async () => {
    try {
      const response = await axios.get('/api/tags/');
      setTags(response.data);
    } catch (error) {
      console.error('Error fetching tags:', error);
    }
  };

  return (
    <div>
      <h1>Tags</h1>
      <ul>
        {tags.map(tag => (
          <li key={tag.id}>{tag.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default TagList;