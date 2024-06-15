'use client'
import React, { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const StartScraping: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [maxDepth, setMaxDepth] = useState('2');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/start-scraping', { searchTerm, maxDepth });
      toast.success(response.data.message);
    } catch (error) {
      toast.error('Failed to start scraping process');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Enter search term"
      />
      <select
        value={maxDepth}
        onChange={(e) => setMaxDepth(e.target.value)}
      >
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6</option>
      </select>
      <button type="submit">Start Scraping</button>
    </form>
  );
};

export default StartScraping;