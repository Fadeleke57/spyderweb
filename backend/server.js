const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(bodyParser.json());
app.use(cors());

app.post('/api/start-scraping', async (req, res) => {
  const { searchTerm } = req.body;
  try {
    // Start the Scrapy process using Docker API
    const response = await axios.post(`http://localhost:6800/scrapy/schedule.json`, {
      project: 'spyderweb',
      spider: 'time',
      search_term: searchTerm
    });
    res.json({ message: 'Scraping started successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Failed to start scraping process' });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));