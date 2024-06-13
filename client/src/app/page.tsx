'use client'

import React, { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import styles from './page.module.css'

const StartScraping = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSubmit = async (e : any) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/start-scraping', { searchTerm });
      toast.success(response.data.message);
    } catch (error) {
      toast.error('Failed to start scraping process');
    }
  };

  return (
    <div className={styles.main}>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Enter search term"
        />
        <button type="submit">Start Scraping</button>
      </form>
    </div>
  );
};

export default StartScraping;