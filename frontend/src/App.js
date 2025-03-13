import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AdminPanel from './components/AdminPanel';
import BlogPost from './components/BlogPost';
import CategoryList from './components/CategoryList';
import TagList from './components/TagList';
import ThemeToggle from './components/ThemeToggle';

function App() {
  return (
    <Router>
      <div className="App">
        <ThemeToggle />
        <Routes>
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/posts/:id" element={<BlogPost />} />
          <Route path="/categories" element={<CategoryList />} />
          <Route path="/tags" element={<TagList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;