'use client'

import React, { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const StartScraping: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/start-scraping', { searchTerm });
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
      <button type="submit">Start Scraping</button>
    </form>
  );
};

export default StartScraping;