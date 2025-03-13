import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function BlogPost() {
  const { id } = useParams();
  const [post, setPost] = useState(null);

  useEffect(() => {
    fetchPost();
  }, [id]);

  const fetchPost = async () => {
    try {
      const response = await axios.get(`/api/posts/${id}/`);
      setPost(response.data);
    } catch (error) {
      console.error('Error fetching post:', error);
    }
  };

  if (!post) return <div>Loading...</div>;

  return (
    <div>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
      {post.image && <img src={`http://localhost:8000${post.image}`} alt={post.title} />}
      {post.video && <video controls><source src={`http://localhost:8000${post.video}`} type="video/mp4" /></video>}
      <p>Categories: {post.categories.map(cat => cat.name).join(', ')}</p>
      <p>Tags: {post.tags.map(tag => tag.name).join(', ')}</p>
    </div>
  );
}

export default BlogPost;