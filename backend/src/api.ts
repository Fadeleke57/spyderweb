import express from 'express';
import { spawn } from 'child_process';
import dotenv from 'dotenv';

dotenv.config();

const router = express.Router();

router.get('/start-scraping', (req, res) => {
  res.status(200).json({ message: 'Hello! Start scraping with a POST request' });
});

router.post('/start-scraping', (req, res) => {
  console.log('Received request to start scraping');
  const { searchTerm } = req.body;
  if (!searchTerm) {
    return res.status(400).json({ message: 'searchTerm is required' });
  }

  const scrapyContainer = 'spyderweb-scrapy-1'; // in docker desktop
  const scrapyCommand = 'scrapy';
  const scrapyArgs = ['crawl', 'time', '-a', `search_term="${searchTerm}"`];
  const dockerArgs = ['exec', scrapyContainer, scrapyCommand, ...scrapyArgs];

  console.log('Starting Scrapy process with the following details:');
  console.log(`docker command: docker ${dockerArgs.join(' ')}`);

  const scrapyProcess = spawn('docker', dockerArgs, { 
    shell: true
  });

  let processOutput = '';

  scrapyProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
    processOutput += data.toString();
  });

  scrapyProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    processOutput += data.toString();
  });

  scrapyProcess.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    if (!res.headersSent) {
      if (code === 0) {
        res.status(200).json({ message: 'Scraping process started successfully', output: "Graph should be displayed now!" });
      } else {
        res.status(500).json({ message: 'Failed to start scraping process', output: processOutput });
      }
    }
  });

  scrapyProcess.on('error', (error) => {
    console.error(`error: ${error.message}`);
    if (!res.headersSent) {
      res.status(500).json({ message: 'Failed to start scraping process', error: error.message });
    }
  });
});

export default router;