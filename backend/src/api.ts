import express from 'express';
import { spawn } from 'child_process';
import dotenv from 'dotenv';

dotenv.config();

const router = express.Router();

router.post('/api/start-scraping', (req, res) => {
  const { searchTerm } = req.body;
  if (!searchTerm) {
    return res.status(400).json({ message: 'searchTerm is required' });
  }

  const scrapyProjectDir = process.env.SCRAPY_PROJECT_DIR || '/app/news_crawler';
  const scrapyCommand = 'scrapy';
  const scrapyArgs = ['crawl', 'time', '-a', `search_term=${searchTerm}`];
  
  console.log('Starting Scrapy process with the following details:');
  console.log(`cwd: ${scrapyProjectDir}`);
  console.log(`command: ${scrapyCommand}`);
  console.log(`args: ${scrapyArgs.join(' ')}`);

  const scrapyProcess = spawn(scrapyCommand, scrapyArgs, {
    cwd: scrapyProjectDir,
    shell: true,
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
        res.status(200).json({ message: 'Scraping process started successfully', output: processOutput });
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