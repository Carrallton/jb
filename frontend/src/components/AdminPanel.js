import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AdminPanel() {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({
    title: '',
    content: '',
    image: null,
    video: null,
    categories_ids: [],
    tags_ids: [],
  });
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);

  useEffect(() => {
    fetchPosts();
    fetchCategories();
    fetchTags();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await axios.get('/api/posts/');
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get('/api/categories/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await axios.get('/api/tags/');
      setTags(response.data);
    } catch (error) {
      console.error('Error fetching tags:', error);
    }
  };

  const handleInputChange = (e) => {
    setNewPost({
      ...newPost,
      [e.target.name]: e.target.value,
    });
  };

  const handleFileChange = (e) => {
    setNewPost({
      ...newPost,
      [e.target.name]: e.target.files[0],
    });
  };

  const handleSelectChange = (e, field) => {
    const values = Array.from(e.target.selectedOptions, option => option.value);
    setNewPost({
      ...newPost,
      [field]: values,
    });
  };

  const handleQuillChange = (value) => {
    setNewPost({
      ...newPost,
      content: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', newPost.title);
    formData.append('content', newPost.content);
    if (newPost.image) formData.append('image', newPost.image);
    if (newPost.video) formData.append('video', newPost.video);
    formData.append('categories_ids', JSON.stringify(newPost.categories_ids));
    formData.append('tags_ids', JSON.stringify(newPost.tags_ids));

    try {
      await axios.post('/api/posts/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      fetchPosts();
      setNewPost({
        title: '',
        content: '',
        image: null,
        video: null,
        categories_ids: [],
        tags_ids: [],
      });
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  const handleEdit = async (postId) => {
    const post = posts.find(p => p.id === postId);
    if (!post) return;

    setNewPost({
      title: post.title,
      content: post.content,
      image: null,
      video: null,
      categories_ids: post.categories.map(cat => cat.id),
      tags_ids: post.tags.map(tag => tag.id),
    });

    // Remove the post from the list and re-fetch posts
    setPosts(posts.filter(p => p.id !== postId));
  };

  return (
    <div>
      <h1>Admin Panel</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="title"
          placeholder="Title"
          value={newPost.title}
          onChange={handleInputChange}
        />
        <input
          type="file"
          name="image"
          onChange={handleFileChange}
        />
        <input
          type="file"
          name="video"
          onChange={handleFileChange}
        />
        <select multiple value={newPost.categories_ids} onChange={(e) => handleSelectChange(e, 'categories_ids')}>
          {categories.map(category => (
            <option key={category.id} value={category.id}>{category.name}</option>
          ))}
        </select>
        <select multiple value={newPost.tags_ids} onChange={(e) => handleSelectChange(e, 'tags_ids')}>
          {tags.map(tag => (
            <option key={tag.id} value={tag.id}>{tag.name}</option>
          ))}
        </select>
        <button type="submit">Create/Edit Post</button>
      </form>
      <ul>
        {posts.map(post => (
          <li key={post.id}>
            <h2>{post.title}</h2>
            <p>{post.content}</p>
            {post.image && <img src={`http://localhost:8000${post.image}`} alt={post.title} />}
            {post.video && <video controls><source src={`http://localhost:8000${post.video}`} type="video/mp4" /></video>}
            <p>Categories: {post.categories.map(cat => cat.name).join(', ')}</p>
            <p>Tags: {post.tags.map(tag => tag.name).join(', ')}</p>
            <button onClick={() => handleEdit(post.id)}>Edit</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AdminPanel;